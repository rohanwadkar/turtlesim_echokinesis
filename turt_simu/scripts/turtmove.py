#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist

from turtlesim.srv import Spawn, SpawnRequest

from std_msgs.msg import Bool

import sys

pub_slave = rospy.Publisher('/my_new_turtle/cmd_vel', Twist, queue_size=10)

global x

pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def move_turtle(lin_vel,ang_vel):

    rospy.init_node('move_turtle', anonymous=True)
    # pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz
 
    vel = Twist()


    while not rospy.is_shutdown():
        
        vel.linear.x = lin_vel
        vel.linear.y = 0
        vel.linear.z = 0

        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = ang_vel



        rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)

        pub.publish(vel)

        rate.sleep()

def spawner_client(xcoord, ycoord):

    rospy.wait_for_service('/spawn')

    spawn_roh = rospy.ServiceProxy('/spawn', Spawn)

    # Create a request message
    request = SpawnRequest()
    request.x = xcoord
    request.y = ycoord
    request.theta = 0.0
    request.name = "my_new_turtle"

    # Call the service to spawn the turtle
    response = spawn_roh(request)

    rospy.loginfo("Spawned turtle with name: %s", response.name)


def mast_vel_cb(msg):
    global x 
    x= msg
    print(x)
    
def follow_master_cb(msg):

    print(msg.data)

    vel_ = Twist()
    vel_ = x 

    if msg.data == True:
        print("I'm inside True")
        pub_slave.publish(vel_)
        pub.publish(vel_)
    

def follow_master():
    
    rospy.init_node('move_turtle', anonymous=True)
    rospy.Subscriber('/follow_master', Bool, follow_master_cb)
    rospy.Subscriber('/turtle1/cmd_vel', Twist, mast_vel_cb)

    rospy.spin()
    


if __name__ == '__main__':
    try:
        #move_turtle(float(sys.argv[1]),float(sys.argv[2]))
        spawner_client(float(sys.argv[1]), float(sys.argv[2]))
        follow_master()
    except rospy.ROSInterruptException:
        pass