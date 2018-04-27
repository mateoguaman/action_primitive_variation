#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def scenario():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('scenario', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        button_1_state = "not pressed" # BUTTON.get_state()
        button_2_state = "pressed" # BUTTON.get_state()
        object_c_location = "x y z" # BUTTON.get_location()

        state_info = "BUTTON 1: " + button_1_state + ", BUTTON 2: " + button_2_state + ", OBJECT: " + object_c_location

        rospy.loginfo(state_info)
        pub.publish(state_info)
        # rate.sleep() # Every time a state chagne message is pubished from the ObtainObject

if __name__ == '__main__':
    try:
        scenario()
    except rospy.ROSInterruptException:
        pass