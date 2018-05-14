#!/usr/bin/env python
# Modified from RethinkRobotics website

import argparse
import struct
import sys
import copy

import pyddl

import rospy
import rospkg
import gazebo_msgs

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

from std_msgs.msg import (
    String,
    Header,
    Empty,
)

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

import baxter_interface


from gazebo_msgs.msg import LinkStates

##################################################
################### STATE INFO ###################
class ScenarioElement(object):
    def __init__(self, _name):
        self.name = _name # string
        self. location = 0
        self.state = "N/A"

    def setLocation(self, _location):
        self.location = _location

    def setState(self, _state):
        self.state = _state

    def print_data(self):
        print("Name: ")
        print(self.name)
        print("Location: ")
        print(self.location)
        print("State: ")
        print(self.state)
##################################################
##################################################

class RobotBrain(object):
    def __init__(self):
        self.robot_name = "Baxter" # string
        # self.objects = ['ground_plane::link', 
        #                 'baxter::base', 
        #                 'baxter::head', 
        #                 'baxter::left_upper_shoulder', 
        #                 'baxter::left_lower_shoulder', 
        #                 'baxter::left_upper_elbow', 
        #                 'baxter::left_lower_elbow', 
        #                 'baxter::left_upper_forearm', 
        #                 'baxter::left_lower_forearm', 
        #                 'baxter::left_wrist', 

        #                 'baxter::l_gripper_l_finger', 
        #                 'baxter::l_gripper_r_finger', 
        #                 'baxter::right_upper_shoulder', 
        #                 'baxter::right_lower_shoulder', 
        #                 'baxter::right_upper_elbow', 
        #                 'baxter::right_lower_elbow', 
        #                 'baxter::right_upper_forearm', 
        #                 'baxter::right_lower_forearm', 
        #                 'baxter::right_wrist', 
        #                 'baxter::r_gripper_l_finger', 

        #                 'baxter::r_gripper_r_finger', 
        #                 'cafe_table::link', 
        #                 'grey_wall::link', 
        #                 'block1::block', 
        #                 'block2::block', 
        #                 'block3::block']

        # self.left_button_location = 0
        # self.right_button_location = 0
        # self.object_location = 0
        # self.grey_wall_location = 0
        # self.cafe_table_location = 0
        # self.r_gripper_location = 0
        # self.l_gripper_location  = 0

        # self.left_button_pressed = False
        # self.right_button_pressed = False

        self.left_button = ScenarioElement("left_button")
        self.right_button = ScenarioElement("right_button")
        self.object = ScenarioElement("object")
        self.grey_wall = ScenarioElement("grey_wall")
        self.cafe_table = ScenarioElement("cafe_table")
        self.r_gripper = ScenarioElement("r_gripper")
        self.l_gripper  = ScenarioElement("l_gripper")

        self.objects = []
        self.objects.append(self.left_button)
        self.objects.append(self.right_button)
        self.objects.append(self.object)
        self.objects.append(self.grey_wall)
        self.objects.append(self.cafe_table)
        self.objects.append(self.r_gripper)
        self.objects.append(self.l_gripper)


    def observe_state(self):
        self.evaluate_discrete_data()

    def print_data(self):

        for obj in self.objects:
            obj.print_data()

        # if(self.left_button_pressed):
        #     print("Left Button Pressed")
        # if(self.right_button_pressed):
        #     print("Right Button Pressed")

        # print("Left Button Location: ")
        # print(self.left_button_location)

        # print("Right Button Location: ")
        # print(self.right_button_location)

        # print("Object Location: ")
        # print(self.object_location)

        # print("Grey Wall Location: ")
        # print(self.grey_wall_location)
        
        # print("Cafe Table Location: ")
        # print(self.cafe_table_location)

        # print("Right Gripper Location: ")
        # print(self.r_gripper_location)

        # print("Left Gripper Location: ")
        # print(self.l_gripper_location)

    def evaluate_discrete_data(self):
        if(abs(self.l_gripper_location.x - self.left_button_location.x) < 0.01):
            self.left_button_pressed = True
        if(abs(self.r_gripper_location.x - self.left_button_location.x) < 0.01):
            self.left_button_pressed = True
        if(abs(self.l_gripper_location.x - self.right_button_location.x) < 0.01):
            self.right_button_pressed = True
        if(abs(self.r_gripper_location.x - self.right_button_location.x) < 0.01):
            self.right_button_pressed = True

    # def update(self, data):


    def callback(self, data):
        
        names = data.name
        poses = data.pose

        left_button_index = len(data.name) - 1
        right_button_index = left_button_index -1
        object_index = right_button_index - 1 
        grey_wall_index = object_index -1 
        cafe_table_index = grey_wall_index - 1 
        l_gripper_index = cafe_table_index - 1 
        r_gripper_index = l_gripper_index - 10

        # self.left_button_location = poses[left_button_index].position
        # self.right_button_location = poses[right_button_index].position
        # self.object_location = poses[object_index].position
        # self.grey_wall_location = poses[grey_wall_index].position
        # self.cafe_table_location = poses[cafe_table_index].position
        # self.r_gripper_location = poses[r_gripper_index].position
        # self.l_gripper_location =  poses[l_gripper_index].position
        self.left_button.setLocation(poses[left_button_index].position)
        self.right_button.setLocation(poses[right_button_index].position)
        self.object.setLocation(poses[object_index].position)
        self.grey_wall.setLocation(poses[grey_wall_index].position)
        self.cafe_table.setLocation(poses[cafe_table_index].position)
        self.r_gripper.setLocation(poses[r_gripper_index].position)
        self.l_gripper.setLocation(poses[l_gripper_index].position)

        # self.observe_state()
        self.print_data()

    def brain(self):
        rospy.init_node("robot_brain", anonymous=True)
        sub = rospy.Subscriber("gazebo/link_states", LinkStates, self.callback)

        # brain = RobotBrain()
        rospy.spin() #simply keeps python from exiting until this node is stopped
        # while not rospy.is_shutdown():
        #     rospy.spin()

if __name__ == '__main__':
    brain = RobotBrain()
    brain.brain()