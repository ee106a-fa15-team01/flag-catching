import rospy
import exp_quat_func as eqf
from numpy.linalg import inv
import numpy as np
import math
from geometry_msgs.msg import Transform, Vector3, Twist

listener = None
zumy_vel = None
zumy_artag = None
origin = None

def stop():
    zumy_vel.publish(Twist(Vector3(0.0,0,0),Vector3(0,0,0)))

def goto(point, v, w):
    rate = rospy.Rate(10)
    arrived = False
    while not arrived:
        x, y = trans_zumy(point)
        if math.hypot(x, y) > 0.2:
            continue
        print 'rotating', (x, y)
        if x<-0.01 or abs(y) >= .035:
            ww = math.copysign(w, y)
            #if abs(v) > .15:
            #   v = math.copysign(.15, y)
            twist=Twist(Vector3(0,0,0),Vector3(0,0,ww))
        else:
            twist=Twist(Vector3(v,0,0),Vector3(0,0,0))
            arrived = True
        zumy_vel.publish(twist)
        rate.sleep()
        
    arrived = False
    while not arrived:
        x, y = trans_zumy(point)
        if math.hypot(x, y) > 0.2:
            continue
        print (x, y)
        if x <= 0.01:
            twist=Twist(Vector3(v/2.0,0,0),Vector3(0,0,0))
            arrived = True
        elif abs(y) >= .01:
            ww = math.copysign(.03, y)
            twist=Twist(Vector3(v,0,0),Vector3(0,0,ww))
        else:
            twist=Twist(Vector3(v,0,0),Vector3(0,0,0))
        #print twist
        zumy_vel.publish(twist)
        rate.sleep()

def trans_zumy(point):
    trans, rot = getrawcoord(zumy_artag)
    (omega,theta) = eqf.quaternion_to_exp(rot)
    g0a = eqf.create_rbt(omega, theta, trans)
    g0a_inv = inv(g0a)
    (x,y) = point
    p0b = np.array([[x],[y],[0],[1]])
    pab = np.dot(g0a_inv,p0b)
    trans_z = (pab[0,0],pab[1,0])
    return trans_z

def getrawcoord(ar_tag):
    now = rospy.Time.now()
    try:
        listener.waitForTransform(origin, 'ar_marker_' + str(ar_tag), rospy.Time(), rospy.Duration(1))
        trans, rot = listener.lookupTransform(origin, 'ar_marker_' + str(ar_tag), rospy.Time())
    except:
	print ar_tag
	raise
    return trans, rot
