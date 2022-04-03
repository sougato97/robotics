#!/usr/bin/env python 

#from re import sub
import rospy
from rospy.client import get_param
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped
from ackermann_msgs.msg import AckermannDrive

#Twist.linear.x = 2


#get car parameters
#max_speed = get_param("max_speed")
#max_steering_angle = get_param("max_steering_angle")

pub = None

def callback(msg):
    regions = {
        # Taking LiDar distance info from its range array which rotates around 360 degrees & it has 1080pts in 2pi degrees. front direction is the x axis
        'right' : min(min(msg.ranges[170:370]), 5), # east direction
        'diagright' : min(min(msg.ranges[370:440]), 5), # northast direction
        'front' : min(min(msg.ranges[440:640]), 5), # north direction
        'diagleft' : min(min(msg.ranges[640:710]), 5), # northwest direction
        'left' : min(min(msg.ranges[710:910]), 5), # west direction
        'back' : min(min(msg.ranges[710:910]), 5),  # south direction
        'b_diagright' : min(min(msg.ranges[370:440]), 5),  # southwest direction
        'b_diagleft' : min(min(msg.ranges[640:710]), 5),  # southeast direction
    }
    header = msg.header
    #print(len(msg.ranges))
    move(regions,header)

def move(regions,header):
    drive_msg = AckermannDrive()
    drive_st_msg = AckermannDriveStamped()
    drive_msg.speed = 2 # This is the default speed
    #steering_angle_velocity1 = 0

    #Listen for odom messages
    #odom_sub = rospy.Subscriber('/odom', Odometry, callback)
    
    #std::string drive_topic, odom_topic;
    #n.getParam("evader_drive_topic", drive_topic);


    if regions['front'] > 1 and regions['diagleft'] > 1 and regions['diagright'] > 1:
        drive_msg.speed = 2 # this is the linear velocity 
        drive_msg.steering_angle = 0
    elif regions['front'] > 1 and regions['diagleft'] > 1 and regions['diagright'] < 1:
        drive_msg.speed = 0.5
        drive_msg.steering_angle = 0.4
    elif regions['front'] > 1 and regions['diagleft'] < 1 and regions['diagright'] > 1:
        drive_msg.speed = 0.5
        drive_msg.steering_angle = -0.4
    elif regions['front'] > 1 and regions['diagleft'] < 0.5 and regions['diagright'] < 0.5: # Not needed though
        drive_msg.speed = 0.5
        drive_msg.steering_angle = 0
    elif regions['front'] < 1 and regions['diagleft'] > 1 and regions['diagright'] > 1: # Need to go backwards
        drive_msg.speed = 0.5
        drive_msg.steering_angle = 0.3
    elif regions['front'] < 1 and regions['diagleft'] > 1 and regions['diagright'] < 1: # Need to go backwards
        drive_msg.speed = 0.5
        drive_msg.steering_angle = 0.3
    elif regions['front'] < 1 and regions['diagleft'] < 1 and regions['diagright'] > 1: # Need to go backwards
        drive_msg.speed = 0.5
        drive_msg.steering_angle = -0.3
    elif regions['front'] < 1 and regions['diagleft'] < 1 and regions['diagright'] < 1: # Need to go backwards
        drive_msg.speed = 0.5     
        drive_msg.steering_angle = 3
    else:
        rospy.loginfo(regions)


    #set drive message in drive stamped message
    drive_st_msg.drive = drive_msg
    drive_st_msg.header = header

    #publish AckermannDriveStamped message to drive topic
    pub.publish(drive_st_msg)

def main():
    global pub
    rospy.init_node('evader')
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    pub = rospy.Publisher('/evader_drive', AckermannDriveStamped, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    main()
