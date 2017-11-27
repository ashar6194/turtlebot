from __future__ import print_function
import numpy as np
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cmath
from geometry_msgs.msg import Twist

class GoForward():
    def __init__(self):
        rospy.init_node('GoForward', anonymous=False)
    	rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.ang_vel = 0.000;
        self.lin_vel = 0.000;
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        move_cmd = Twist()
        r = rospy.Rate(10)
        self.bridge = CvBridge()
        self.rgb_image = 0
        self.depth_image = 0
        self.object_seg = 0
        self.mask = 0

        rospy.Subscriber("/camera/rgb/image_raw",Image,self.RGBCallback)
        rospy.Subscriber("/camera/depth/image_raw",Image,self.DepthCallback)

        while not rospy.is_shutdown():
            cv2.imshow("RGB Image window", self.rgb_image)
            cv2.imshow("Segmented Object", self.object_seg)
            cv2.waitKey(10)
            move_cmd.linear.x = self.lin_vel
            move_cmd.angular.z = self.ang_vel
            self.cmd_vel.publish(move_cmd)
            r.sleep()
        
        rospy.spin()
        
    def RGBCallback(self,data):
        
        self.rgb_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        low = np.array([15, 40, 70], dtype = 'uint8')
        high = np.array([30, 60, 90], dtype = 'uint8')
        self.mask = cv2.inRange(self.rgb_image, low, high)
        self.object_seg = cv2.bitwise_and(self.rgb_image, self.rgb_image, mask = self.mask)

        # To find centroid of the object
        centre_image = np.array(self.mask);
        max_y, max_x, channels = np.shape(self.rgb_image)
        ind_x = np.where(np.sum(centre_image, axis = 0) != 0)
        ind_y = np.where(np.sum(centre_image, axis = 1) != 0)
        centroid_x = (max(max(ind_x)) + min(min(ind_x))) / 2;
        centroid_y = (max(max(ind_y)) + min(min(ind_y))) / 2;
        print (centroid_x, centroid_y, max_x/2, max_y/2)

        self.object_seg[centroid_y, centroid_x, :] = (0, 0, 255)
        
        self.ang_vel = -0.01* (centroid_x - (max_x/2))
        if ( self.ang_vel >= 0.05 ):
            self.ang_vel = 0.05
        elif( self.ang_vel <= -0.05 ):
            self.ang_vel = -0.05

            
        self.lin_vel = 0.01* (centroid_y - (max_y/2))
        if ( self.lin_vel >= 0.05 ):
            self.lin_vel = 0.05
        elif( self.lin_vel <= -0.05 ):
            self.lin_vel = -0.05

    def DepthCallback(self,data):
        a = self.bridge.imgmsg_to_cv2(data, "32FC1")
        dst = np.zeros(shape=(5,2))
        self.depth_image = cv2.normalize(a,dst,0,1,cv2.NORM_MINMAX)

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        GoForward()
    except:
        rospy.loginfo("GoForward node terminated.")