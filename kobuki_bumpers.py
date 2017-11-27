
import roslib
import rospy
from kobuki_msgs.msg import BumperEvent

class kobuki_bumper():

	def __init__(self):
		rospy.init_node("kobuki_bumper")		

		#monitor kobuki's bumper events
		rospy.Subscriber("/mobile_base/events/bumper",BumperEvent,self.BumperEventCallback)

		#rospy.spin() tells the program to not exit until you press ctrl + c.  If this wasn't there... it'd subscribe and then immediatly exit (therefore stop "listening" to the thread).
		rospy.spin();

	
	def BumperEventCallback(self,data):
	    if ( data.state == BumperEvent.RELEASED ) :
		state = "released"
	    else:
		state = "pressed"
	    if ( data.bumper == BumperEvent.LEFT ) :
		bumper = "Left_Bumper"
	    elif ( data.bumper == BumperEvent.RIGHT ) :
		bumper = "Right_Bumper"
	    else:
		bumper = "Center_bumper"
	    rospy.loginfo("%s was %s."%(bumper, state))
	    return bumper, state
	

if __name__ == '__main__':
	try:
		kobuki_bumper()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")
