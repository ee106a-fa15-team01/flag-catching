import tf
import rospy
import sys
from geometry_msgs.msg import Twist
import pf, epf, gpf
from flag_catching.msg import Arrive
import zumy_control

listener = None
unit = 0.05
status = False

def convert(trans):
    x, y, z = trans
    return int(x/unit+.5), int(y/unit+.5)

def getcoord(ar_tag):
    trans, rot = zumy_control.getrawcoord(ar_tag)
    return convert(trans)

def follow_ar_tag():
    global listener, status
    while not rospy.is_shutdown():
        zumy_control.stop()
        raw_input('press enter to do path planning')
        status = False
        while True:
            try:
                dst_coord = getcoord(goal_artag)
                src_coord = getcoord(zumy_artag)
                obst_coords = [getcoord(i) for i in obstacle_artags]
                print dst_coord, src_coord, obst_coords
                if is_arrived():
                    zumy_control.stop()
                    break
                if status == True:
                    break
                f = epf.EuclidField(
                    (field_width, field_height),   # width x height
                    dst_coord,    # goal
                    obst_coords # obstacles
                )
                try:
                    im = pf.field_to_image(f)
                    pf.draw_path(im, [src_coord])
                except:
                    pass
                #im.show()
                im.resize((800, 800)).save('out.png')
                point = pf.find_nextstep(f, src_coord)
                print 'going to', point
                zumy_control.goto(ftrans(point))
                #raw_input('press enter for next step')
            except tf.Exception:
                zumy_control.stop()
                continue
        while True:
            try:
                src_coord = getcoord(zumy_artag)
                obst_coords = [getcoord(i) for i in obstacle_artags]
                print src_coord, obst_coords
                if is_home():
                    pub.publish(Arrive('GameOver'))
                    status = True
                if status==True:
                    break
                f = gpf.EuclidField(
                    (field_width, field_height),   # width x height  # goal
                    obst_coords # obstacles
                )
                try:
                    im = pf.field_to_image(f)
                    pf.draw_path(im, [src_coord])
                except:
                    pass
                #im.show()
                im.resize((800, 800)).save('out.png')
                point = pf.find_nextstep(f, src_coord)
                print 'going to', point
                zumy_control.goto(ftrans(point))
                #raw_input('press enter for next step')
            except tf.Exception:
                zumy_control.stop()
                continue

def ftrans(point):    
    return (point[0]*unit, point[1]*unit)

def is_arrived():
    dstx, dsty = getcoord(goal_artag)
    srcx, srcy = getcoord(zumy_artag)
    if abs(dstx-srcx)<=2 and abs(dsty-srcy)<=2:
       return True
    else:
       return False
       
def is_home():
    srcx, srcy = getcoord(zumy_artag)
    if srcx<=1:
       return True
    else:
       return False

def callback(message):
    global status
    print message.end
    if message.end == 'GameOver':
       status = True
       
if __name__=='__main__':
    try:
        zumy_name = sys.argv[1]
        rospy.init_node(zumy_name + '_goal')
        zumy_control.origin = 'ar_marker_' + sys.argv[2]
        margin_artag = int(sys.argv[3])
        goal_artag = int(sys.argv[4])
        zumy_control.listener = tf.TransformListener()
        zumy_control.zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy_name, Twist, queue_size=2)
        zumy_artag = zumy_control.zumy_artag = int(sys.argv[5])
        obstacle_artags = [int(i) for i in sys.argv[6:]]
    except IndexError:
        print "args: zumy_name origin margin goal zumy_artag [obstacle_artag ...]"
        sys.exit()
    field_height, field_width = [i+1 for i in getcoord(margin_artag)]
    pub = rospy.Publisher('Game_status', Arrive, queue_size=10)
    rospy.Subscriber("Game_status",Arrive, callback)
    follow_ar_tag()
    rospy.spin()
