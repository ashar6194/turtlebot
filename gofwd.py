
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent

class GoForward():
    def __init__(self):
        rospy.init_node('GoForward', anonymous=False)
    	rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.state="RELEASED"

        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        move_cmd = Twist()
        r = rospy.Rate(10)

        rospy.Subscriber("/mobile_base/events/bumper",BumperEvent, self.BumperEventCallback)
	    

        while not rospy.is_shutdown():
            if ( self.state == "RELEASED"):
                move_cmd.linear.x = 0.3
                move_cmd.angular.z = 0
                self.cmd_vel.publish(move_cmd)
                r.sleep()
            else:
                rospy.loginfo("I am Stuck, Trying to rotate!")
                move_cmd.linear.x = 0
                move_cmd.angular.z = 0.3
                self.cmd_vel.publish(move_cmd)
                r.sleep()

        rospy.spin()
        
                        
        

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