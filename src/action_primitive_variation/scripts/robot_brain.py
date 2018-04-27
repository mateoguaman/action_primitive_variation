#!/usr/bin/env python
# Modified from RethinkRobotics website

import argparse
import struct
import sys
import copy

import pyddl

import rospy
import rospkg

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

class RobotBrain(object):
    def __init__(self):
        self.robot_name = "Baxter" # string

    def observe_state(self):
        print("Observing state")


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def brain():
    rospy.init_node("robot_brain", anonymous=True)
    # Wait for the All Clear from emulator startup

    rospy.Subscriber("chatter", String, callback)
    brain = RobotBrain()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    brain()