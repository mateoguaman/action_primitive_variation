#!/usr/bin/env python
# Modified from RethinkRobotics website

import argparse
import struct
import sys
import copy

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

class SearchAndRescueWorld(object):
    def __init__(self, limb, hover_distance = 0.15, verbose=True):
        ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
        self._iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
        rospy.wait_for_service(ns, 5.0)
        # verify robot is enabled
        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()
        self.object_c = "N/A"
        self.button_1 = "N/A"
        self.button_2 = "N/A"
        self.goal = "N/A"


def load_gazebo_models(table_pose=Pose(position=Point(x=1.0, y=0.0, z=0.0)),
                       table_reference_frame="world",
                       block1_pose=Pose(position=Point(x=0.8, y=-0.0065, z=0.7825)),
                       block2_pose=Pose(position=Point(x=0.6050, y=-0.2965, z=0.7825)),
                       block3_pose=Pose(position=Point(x=0.6050, y=0.1265, z=0.7825)),
                       block_reference_frame="world",
                       grey_wall_pose=Pose(position=Point(x=0.79, y=-0.0065, z=0.7825)),
                       grey_wall_reference_frame="world"):
    # Get Models' Path
    model_path = rospkg.RosPack().get_path('baxter_sim_examples')+"/models/"
    # Load Table SDF
    table_xml = ''
    with open (model_path + "cafe_table/model.sdf", "r") as table_file:
        table_xml=table_file.read().replace('\n', '')
    grey_wall_xml = ''
    with open (model_path + "grey_wall/model.sdf", "r") as grey_wall_file:
        grey_wall_xml=grey_wall_file.read().replace('\n', '')
    # Load Block URDF
    block1_xml = ''
    with open (model_path + "block/model.urdf", "r") as block_file:
        block_xml=block_file.read().replace('\n', '')
    block2_xml = ''
    with open (model_path + "block/model.urdf", "r") as block_file:
        block_xml=block_file.read().replace('\n', '')
    block3_xml = ''
    with open (model_path + "block/model.urdf", "r") as block_file:
        block_xml=block_file.read().replace('\n', '')
    # Spawn Table SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')

    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("cafe_table", table_xml, "/",
                             table_pose, table_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_urdf = spawn_sdf("grey_wall", grey_wall_xml, "/",
                               grey_wall_pose, grey_wall_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))
    # Spawn Block URDF
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    

    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf("block1", block_xml, "/",
                               block1_pose, block_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    object_c = block1_pose

    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf("block2", block_xml, "/",
                               block2_pose, block_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    button_1 = block2_pose

    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf("block3", block_xml, "/",
                               block3_pose, block_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))
    button_2 = block2_pose


def delete_gazebo_models():
    # This will be called on ROS Exit, deleting Gazebo models
    # Do not wait for the Gazebo Delete Model service, since
    # Gazebo should already be running. If the service is not
    # available since Gazebo has been killed, it is fine to error out
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model("cafe_table")
        resp_delete = delete_model("block")
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

def main():

    rospy.init_node("search_and_rescue")
    load_gazebo_models()
    rospy.wait_for_message("/robot/sim/started", Empty)    

    pub_obj_c = rospy.Publisher('object_c', Pose, queue_size=10)
    pub_button_1 = rospy.Publisher('button_1', Pose, queue_size=10)
    pub_button_2 = rospy.Publisher('button_2', Pose, queue_size=10)

    # obj_info = object_c
    # button_1_info = button_1
    # button_2_info = button_2

    # while not rospy.is_shutdown():
    #     print("\Search-and-rescue mission in action")

    return 0

####################################################################################
    # pub = rospy.Publisher('chatter', String, queue_size=10)
    # rospy.init_node('scenario', anonymous=True)
    # rate = rospy.Rate(10) # 10hz

    # while not rospy.is_shutdown():

    #     button_1_state = "not pressed" # BUTTON.get_state()
    #     button_2_state = "pressed" # BUTTON.get_state()
    #     object_c_location = "x y z" # BUTTON.get_location()

    #     state_info = "BUTTON 1: " + button_1_state + ", BUTTON 2: " + button_2_state + ", OBJECT: " + object_c_location

    #     rospy.loginfo(state_info)
    #     pub.publish(state_info)
        # rate.sleep() # Every time a state chagne message is pubished from the ObtainObject

if __name__ == '__main__':
    sys.exit(main())
