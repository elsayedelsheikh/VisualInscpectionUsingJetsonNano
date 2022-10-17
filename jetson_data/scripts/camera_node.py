#!/usr/bin/env python
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def main():
    try:
        rospy.init_node('cam_streamer')
        bridge = CvBridge()
        img_pub = rospy.Publisher('/camera1/raw_image', Image,queue_size=3)
        rate = rospy.Rate(21)

        ## Camera
        # Camera Display Settings
        dispW = 256
        dispH = 256
        flip  = 2 ## 0 or 2
        # Camera Capture Settings
        capW = 3264
        capH = 2464
        fps = 21
        camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width='+str(capW)+', height='+str(capH)+', format=NV12, framerate='+str(fps)+'/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        cam = cv2.VideoCapture(camSet)

        while not rospy.is_shutdown():
            ret, cv_image = cam.read()
            rospy.loginfo_once("Started Capturing")
            if ret:
                img_msg = bridge.cv2_to_imgmsg(cv_image, "bgr8")
                img_pub.publish(img_msg)
            else:
                rospy.logerr("Not recieving any frames")
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
    finally:
        cam.release()   

if __name__ == "__main__":
    main()