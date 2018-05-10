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

class RobotBrain(object):
    def __init__(self):
        self.robot_name = "Baxter" # string

    def observe_state(self):
        print("Observing state")


def callback(data):
    print("Callback function invoked in robot brain")
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # print(rospy.get_caller_id() + "I heard: ")
    print(data.name)
    # print()

def brain():
    rospy.init_node("robot_brain", anonymous=True)
    # Wait for the All Clear from emulator startup
    # sub = rospy.Subscriber("gazebo_info", String, callback)

    sub = rospy.Subscriber("gazebo/link_states", LinkStates, callback)
    # brain = RobotBrain()
    rospy.spin() #simply keeps python from exiting until this node is stopped
    # while not rospy.is_shutdown():
    #     rospy.spin()

if __name__ == '__main__':
    brain()