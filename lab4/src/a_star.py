#!/usr/bin/env python
import numpy as np
from heapq import *
import math
import rospy
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

# variable declaration
map = np.array([
       [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
       [0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
       [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0],
       [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
       [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
       [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],
       [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
       [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
       [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
       [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
       [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]])

dictionary={} 
start = (1,12)
goal = (13,1)
goalx,goaly = goal
periphery = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

# declaration end
# map = np.loadtxt("map.txt", dtype=int)



def heuristic(start, goal):
    dist = math.sqrt((goal[0] - start[0])**2  + (goal[1] - start[1])**2)
    return dist

def periphery_fn(dict):
    
    for i, j in periphery:
        neighbor = dict['current'][0] + i, dict['current'][1] + j
        new_gn = dict['gn'][dict['current']] + heuristic(dict['current'], neighbor)
            
        if 0 <= neighbor[0] < map.shape[1]:
            if 0 <= neighbor[1] < map.shape[0]:
                if map[neighbor[1]][neighbor[0]] == 1:
                    continue
            else:
                continue
        else:
            continue

        if neighbor in dict['close'] and new_gn >= dict['gn'].get(neighbor, 0):
            continue

        if  new_gn < dict['gn'].get(neighbor, 0) :
            dict['prior'][neighbor] = dict['current']
            dict['gn'][neighbor] = new_gn
            dict['fn'][neighbor] = new_gn + heuristic(neighbor, goal)
            heappush(dict['open'], (dict['fn'][neighbor], neighbor))  

        elif  neighbor not in [i[1]for i in dict['open']]:
            dict['prior'][neighbor] = dict['current']
            dict['gn'][neighbor] = new_gn
            dict['fn'][neighbor] = new_gn + heuristic(neighbor, goal)
            heappush(dict['open'], (dict['fn'][neighbor], neighbor)) 

#As the path cost is same between all nodes, I didn't implement priority queue/heap. Here each an every step is irreversible... 
#I dont store the prev visited cost, only the cost from the present node is stored.
def astar(map, start, goal):

    #Declaring the variables
    close_set = set() # stores only the key values from a dictionary, done with the help of set() method
    prior = {} # empty dictionary 
    gn = {start:0}
    fn = {start:heuristic(start, goal)}
    open_set = [] # empty list

    heappush(open_set, (fn[start], start))

    while open_set:

        current = heappop(open_set)[1]

        if current == goal:
            data = []
            while current in prior:
                data.append(current)
                current = prior[current]
            data.reverse()
            return data

        close_set.add(current)
        
        thisdict = {
            "map": map,
            "current": current,
            "open": open_set,
            "close": close_set,
            "fn": fn,
            "gn": gn,
            "prior": prior,
            "periphery": periphery
            }
        periphery_fn(thisdict)

    return False

def turn(linear_x, angular_z):
    temp = Twist()
    temp.linear.x = linear_x
    temp.linear.y = 0
    temp.linear.z = 0

    temp.angular.x = 0
    temp.angular.y = 0
    temp.angular.z = angular_z
    return temp

def robot_rotate(error,pub):
    if math.fabs(error) > math.radians(6):
        # rotate
        if error < 0:
            error += math.pi * 2
        elif error > math.pi * 2:
            error -= math.pi * 2
        if error < math.pi:
            # Angular
            pub.publish(turn(0,0.75))
        else: 
            # Angular
            pub.publish(turn(0,-0.75))
    else:
        dictionary["rotate"]=False

def robot_move(data):

    if not dictionary["flag"]:

        position = data.pose.pose.position
        quart_orientation=data.pose.pose.orientation

        actual_orientation = tf.transformations.euler_from_quaternion([quart_orientation.x, quart_orientation.y, quart_orientation.z, quart_orientation.w])[2]

        goalx = dictionary['path'][dictionary['next']][0]-9 + 0.8
        goaly = 10-dictionary['path'][dictionary['next']][1] - 0.8

        calc_orientation = math.atan2(goaly - position.y, goalx - position.x)

        error = calc_orientation - actual_orientation
        if dictionary['rotate']:
            robot_rotate(error,dictionary['pub'])
        # condition of no rotation
        else:
            error=math.sqrt((goalx - position.x)**2+(goaly - position.y)**2)
            if error <= 0.5:
                dictionary["rotate"]=True
                if dictionary['next'] + 1< len(dictionary['path']):
                    dictionary['next'] += 1
                else:
                    dictionary['flag']=True
            else:
                # Linear
                dictionary['pub'].publish(turn(0.75,0)) 


def dictionary_init(rospy):
    dictionary['flag']=False
    dictionary['next']=0
    dictionary["rotate"]=True
    dictionary['pub']= rospy.Publisher('/cmd_vel',Twist,queue_size=1)
    dictionary['path']=astar(map, start, goal)

def change_param(rospy):
    goalx,goaly=rospy.get_param("/goalx"),rospy.get_param("/goaly")
    rospy.delete_param("/goalx")
    rospy.delete_param("/goaly")
    nstart = goal
    goal = (round(goalx+9),round(10-goaly))
    dictionary['path'] = astar(map, nstart, goal)
    dictionary["rotate"] = True
    dictionary['next'] = 0
    dictionary['flag'] = False

if __name__ == '__main__':

    rospy.init_node("robot", anonymous=False)
    dictionary_init(rospy)
    robot_pos_pub = rospy.Subscriber("/base_pose_ground_truth", Odometry,robot_move)

    while not rospy.is_shutdown():
        if dictionary['flag']:
            if rospy.has_param("/goalx") and rospy.has_param("/goaly"):
                change_param(rospy)

        rate = rospy.Rate(2)
        rospy.sleep(1)

