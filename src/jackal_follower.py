#!/usr/bin/env python2

import rospy
from time import sleep
from geometry_msgs.msg import Twist, Pose

rospy.init_node('jackal_controller')
box_pose = Pose()
vel_msg = Twist()

def box_pose_callback(msg):
    global box_pose
    box_pose = msg

def main():
    global box_pose
    global vel_msg

    # Subscriber
    rospy.Subscriber('/box_pose/center', Pose, box_pose_callback)

    # Publisher
    pub = rospy.Publisher('jackal_velocity_controller/cmd_vel', Twist, queue_size=10)

    r = rospy.Rate(10)

    while not rospy.is_shutdown():
        marker_pose = box_pose
        jackal_controller(marker_pose)
        pub.publish(Twist(vel_msg.linear, vel_msg.angular))
        print(vel_msg)

        r.sleep()

    #############################################################
    # Running ROS
    #############################################################
    rospy.spin()        # Spin until ctrl + c

def jackal_controller(marker_pose):
    global vel_msg

    setpoint_x = -0.55
    setpoint_y = 0.05
    error_x = abs(marker_pose.position.x) + setpoint_x
    error_y = setpoint_y - marker_pose.position.y
    Kp_lin = 0.4
    Kp_ang = 0.3

    print(error_x)
    print(error_y)
    print(marker_pose.position.y)

    base_vel = 0.4
    base_ang = 0.5

    #P controller for linear velocity
    if marker_pose.position.x == 0:
        vel_msg.linear.x = 0
    elif marker_pose.position.x < -0.60:
        vel_msg.linear.x = 0
    elif marker_pose.position.x >= -0.60: 
        vel_msg.linear.x = base_vel - error_x * Kp_lin
    else:
        vel_msg.linear.x = 0


    #P controller for angular velocity
    if marker_pose.position.y >= -0.05 and marker_pose.position.y <= 0.015:
        vel_msg.angular.z = 0 
    elif marker_pose.position.y > 0.15:
        vel_msg.angular.z = base_ang + abs(error_y) * Kp_ang
    elif marker_pose.position.y < -0.05:
        vel_msg.angular.z = - base_ang - abs(error_y) * Kp_ang
    else:
        vel_msg.angular.z = 0

    #mid = 0.05
    #when less than -0.1 turn right 
    #when greater than 0.2 turn left (positive)
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
