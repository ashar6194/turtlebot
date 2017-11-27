from __future__ import print_function
import numpy as np
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
  def __init__(self):
    rospy.init_node('image_converter', anonymous=True)
    # self.image_pub = rospy.Publisher("image_topic_2",Image)
    print ('Hey!')
    self.bridge = CvBridge()
    rospy.Subscriber("/camera/rgb/image_raw",Image,self.RGBCallback)
    rospy.Subscriber("/camera/depth/image_raw",Image,self.DepthCallback)
    self.rgb_image = 0
    self.depth_image = 0
    self.object_seg = 0
    self.mask = 0

    while not rospy.is_shutdown():
      cv2.imshow("RGB Image window", self.rgb_image)
      cv2.imshow("Depth Image window", self.depth_image)
      # cv2.imshow("Mask", self.mask)
      cv2.imshow("Segmented Object", self.object_seg)
      cv2.waitKey(10)

    rospy.spin()

  def RGBCallback(self,data):
    self.rgb_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    low = np.array([15, 40, 70], dtype = 'uint8')
    high = np.array([30, 60, 90], dtype = 'uint8')
    self.mask = cv2.inRange(self.rgb_image, low, high)
    self.object_seg = cv2.bitwise_and(self.rgb_image, self.rgb_image, mask = self.mask)

  def DepthCallback(self,data):
    a = self.bridge.imgmsg_to_cv2(data, "32FC1")
    dst = np.zeros(shape=(5,2))
    self.depth_image = cv2.normalize(a,dst,0,1,cv2.NORM_MINMAX)

if __name__ == '__main__':
    try:
        image_converter()
    except:
        rospy.loginfo("GoForward node terminated.")
        print("Shutting down")
        cv2.destroyAllWindows()