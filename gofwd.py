
import rospy
import cmath
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from nav_msgs.msg import Odometry

class GoForward():
    def __init__(self):
        rospy.init_node('GoForward', anonymous=False)
    	rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.state="RELEASED"
        self.a_v = 0.000;
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        move_cmd = Twist()
        r = rospy.Rate(10)

        rospy.Subscriber("/mobile_base/events/bumper",BumperEvent, self.BumperEventCallback)
        rospy.Subscriber("/odom",Odometry, self.OdometryCallback)
	    

        while not rospy.is_shutdown():
            if ( self.state == "RELEASED"):
                move_cmd.linear.x = 0.3
                move_cmd.angular.z = self.a_v
                self.cmd_vel.publish(move_cmd)
                r.sleep()
            else:
                rospy.loginfo("I am Stuck, Trying to rotate!")
                move_cmd.linear.x = 0
                move_cmd.angular.z = 0.3
                self.cmd_vel.publish(move_cmd)
                r.sleep()
        rospy.spin()
        

    def OdometryCallback(self,data):
        # print data.pose.pose
        
        x= data.pose.pose.position.x
        y=data.pose.pose.position.y
        orient = data.pose.pose.orientation.w + data.pose.pose.orientation.z*1j
        z_des = cmath.rect(1, 0)
        z_curr = orient
        z_error = z_des/z_curr
        theta_error = cmath.phase(z_error);
        self.a_v = theta_error
        if (self.a_v > 1):
            self.a_v = 1;
        # print '\ntheta_error is %f' % theta_error
        rospy.loginfo(' Error is :{},' .format(theta_error))

    def BumperEventCallback(self,data):
        if ( data.state == BumperEvent.RELEASED ) :
            self.state = "RELEASED"
        else:
            self.state = "PRESSED"
        
    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        GoForward()
    except:
        rospy.loginfo("GoForward node terminated.")