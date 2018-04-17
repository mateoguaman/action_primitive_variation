#!/usr/bin/env python
# Modified from RethinkRobotics website

import argparse
import struct
import sys
import copy

import pyddl

import rospy
import rospkg

from gazebo_msgs.srv import (
    SpawnModel,
    DeleteModel,
)
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import (
    Header,
    Empty,
)

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

import baxter_interface

class ObtainObject(object):
    def __init__(self, hover_distance = 0.15, verbose=True):
        self._left_limb_name = "left" # string
        self._right_limb_name = "right" # string

        self._hover_distance = hover_distance # in meters
        self._verbose = verbose # bool

        self._left_limb = baxter_interface.Limb("left")
        self._left_gripper = baxter_interface.Gripper("left")

        self._right_limb = baxter_interface.Limb("right")
        self._right_gripper = baxter_interface.Gripper("right")

        ####################################################################################################
        ns_left = "ExternalTools/" + "left" + "/PositionKinematicsNode/IKService"  # Not entirely sure what this is 
        self._iksvc_left = rospy.ServiceProxy(ns_left, SolvePositionIK)               # Not entirely sure what this is 
        ns_right = "ExternalTools/" + "right" + "/PositionKinematicsNode/IKService"  # Not entirely sure what this is 
        self._iksvc_right = rospy.ServiceProxy(ns_right, SolvePositionIK)               # Not entirely sure what this is 
        ####################################################################################################

        rospy.wait_for_service(ns_left, 5.0)
        rospy.wait_for_service(ns_right, 5.0)

        # verify robot is enabled  #########################################################################
        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()

    def move_to_start(self, start_angles=None):
        print("Moving the {0} arm to start pose...".format(self._left_limb_name))
        if not start_angles:
            start_angles = dict(zip(self._joint_names, [0]*7))
        self._guarded_move_to_joint_position(start_angles)
        self.gripper_open(self._left_gripper)
        rospy.sleep(1.0)    
        print("Running. Ctrl-c to quit")


    # Not entirely sure what this is ########################################################################
    # I think its a request for the robot to move to a certain position
    # Takes in a pose and outputs a valid joint solution
    #
    def ik_request(self, gripper, pose):
        hdr = Header(stamp=rospy.Time.now(), frame_id='base')
        ikreq = SolvePositionIKRequest()
        ikreq.pose_stamp.append(PoseStamped(header=hdr, pose=pose))
        try:
            resp = self._iksvc_left(ikreq)
        except (rospy.ServiceException, rospy.ROSException), e:
            rospy.logerr("Service call failed: %s" % (e,))
            return False
        # Check if result valid, and type of seed ultimately used to get solution
        # convert rospy's string representation of uint8[]'s to int's
        resp_seeds = struct.unpack('<%dB' % len(resp.result_type), resp.result_type)
        limb_joints = {}
        if (resp_seeds[0] != resp.RESULT_INVALID):
            seed_str = {
                        ikreq.SEED_USER: 'User Provided Seed',
                        ikreq.SEED_CURRENT: 'Current Joint Angles',
                        ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
                       }.get(resp_seeds[0], 'None')
            if self._verbose:
                print("IK Solution SUCCESS - Valid Joint Solution Found from Seed Type: {0}".format(
                         (seed_str)))
            # Format solution into Limb API-compatible dictionary
            limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
            if self._verbose:
                print("IK Joint Solution:\n{0}".format(limb_joints))
                print("------------------")
        else:
            rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
            return False
        return limb_joints

    def _guarded_move_to_joint_position(self, joint_angles):
        if joint_angles:
            self._left_limb.move_to_joint_positions(joint_angles)
        else:
            rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")

    def gripper_open(self, gripper):
        gripper.open()
        rospy.sleep(1.0)

    def gripper_close(self, gripper):
        gripper.close()
        rospy.sleep(1.0)

    def _approach(self, gripper, pose):
        approach = copy.deepcopy(pose)
        # approach with a pose the hover-distance above the requested pose
        approach.position.z = approach.position.z + self._hover_distance
        joint_angles = self.ik_request(gripper, approach)
        self._guarded_move_to_joint_position(joint_angles)


    # Assumes LEFT gripper/limb
    def _retract(self):
        # retrieve current pose from endpoint
        current_pose = self._left_limb.endpoint_pose()


        ik_pose = Pose()
        ik_pose.position.x = current_pose['position'].x
        ik_pose.position.y = current_pose['position'].y
        ik_pose.position.z = current_pose['position'].z + self._hover_distance
        ik_pose.orientation.x = current_pose['orientation'].x
        ik_pose.orientation.y = current_pose['orientation'].y
        ik_pose.orientation.z = current_pose['orientation'].z
        ik_pose.orientation.w = current_pose['orientation'].w
        joint_angles = self.ik_request(self._left_limb, ik_pose)
        # servo up from current pose
        self._guarded_move_to_joint_position(joint_angles)

    def _servo_to_pose(self, gripper, pose):
        # servo down to release
        joint_angles = self.ik_request(gripper, pose)
        self._guarded_move_to_joint_position(joint_angles)

    def pick(self, gripper, pose):
        # open the gripper
        self.gripper_open(gripper)
        # servo above pose
        self._approach(gripper, pose)
        # servo to pose
        self._servo_to_pose(gripper, pose)
        # close gripper
        self.gripper_close(gripper)
        # retract to clear object
        self._retract()

    # def place(self, pose):
    #     # servo above pose
    #     self._approach(pose)
    #     # servo to pose
    #     self._servo_to_pose(pose)
    #     # open the gripper
    #     self.gripper_open()
    #     # retract to clear object
    #     self._retract()

    #########################################################################################################
    # Our Action Primitives #################################################################################
    # For PDDL planning
    def push_button(self, button_name, gripper, pose):
        print("Pushing button")
        if (gripper == "right"):
            self._approach(self._right_gripper, pose)
            self._servo_to_pose(self._right_gripper, pose)
        else:
            self._approach(self._left_gripper, pose)
            self._servo_to_pose(self._left_gripper, pose)

    def grab_object(self, gripper_name, object_name, pose):
        print("Grabbing object" + object_name)
        if (gripper_name == "right"):
            self.pick(self._right_gripper, pose)
        else:
            self.pick(self._left_gripper, pose)


    def move_object(self, object_name, pose):
        print("Moving object")

    def observe_scenario_state():
        print("Observing scenario state")
        print("Object")   # OBJECT
        print("Button 1") # OBJECT
        print("Button 2") # OBJECT
        print("Wall")     # OBJECT

def main():

    rospy.init_node("obtain_object")

    # Wait for the All Clear from emulator startup
    rospy.wait_for_message("/robot/sim/started", Empty)


    # Use PDDL planner to plan for a goal 
    #
    #

    hover_distance = 0.15 # meters
    # Starting Joint angles for left arm
    starting_joint_angles = {'left_w0': 0.6699952259595108,
                             'left_w1': 1.030009435085784,
                             'left_w2': -0.4999997247485215,
                             'left_e0': -1.189968899785275,
                             'left_e1': 1.9400238130755056,
                             'left_s0': -0.08000397926829805,
                             'left_s1': -0.9999781166910306}
    
    oo = ObtainObject(hover_distance)
    # An orientation for gripper fingers to be overhead and parallel to the obj
    overhead_orientation = Quaternion(
                             x=-0.0249590815779,
                             y=0.999649402929,
                             z=0.00737916180073,
                             w=0.00486450832011)
    block_poses = list()


    # The Pose of the block in its initial location.
    # You may wish to replace these poses with estimates
    # from a perception node.
    block_poses.append(Pose(
        position=Point(x=0.7, y=0.15, z=-0.129),
        orientation=overhead_orientation))
    # Feel free to add additional desired poses for the object.
    # Each additional pose will get its own pick and place.
    block_poses.append(Pose(
        position=Point(x=0.75, y=0.0, z=-0.129),
        orientation=overhead_orientation))
    # Move to the desired starting angles
    oo.move_to_start(starting_joint_angles)
    idx = 0



    button1_pose = Pose(
        position=Point(x=0.6, y=-0.3, z=-0.09),
        orientation=overhead_orientation)
    button2_pose = Pose(
        position=Point(x=0.6, y=0.13, z=-0.09),
        orientation=overhead_orientation)
    object_c_pose = Pose(
        position=Point(x=0.8, y=-0.01, z=-0.129),
        orientation=overhead_orientation)

    # block2_pose=Pose(position=Point(x=0.6925, y=-0.2965, z=0.7825)),
    # block3_pose=Pose(position=Point(x=0.6925, y=0.1265, z=0.7825)),

    # while not rospy.is_shutdown():
        # oo.pick(object_c_pose)
        # print("\nPlacing...")
        # idx = (idx+1) % len(block_poses)
        # oo.place(block_poses[idx])

    print("\nObtaining object...")
    try:
        oo.grab_object("object", "left", object_c_pose)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Move to object failed: %s" % (e,))  
        print("\nObtaining object FAILED")

    print("\nPushing button...")
    try: 
        oo.push_button("button1", "right", button1_pose)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Push button failed: %s" % (e,))  
        print("\nPush button FAILED")

    print("\nRemoving obstruction...")
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model("grey_wall")
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

    print("\nObtaining object...")
    try:
        oo.grab_object("object", "left", object_c_pose)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Move to object failed: %s" % (e,))  
        print("\nObtaining object FAILED")

    return 0

if __name__ == '__main__':
    sys.exit(main())
