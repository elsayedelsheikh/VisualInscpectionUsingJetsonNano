#!/usr/bin/python3
import cv2
import torch
import rospy

def predict(image, model, resolution):
    predictions = []
    result = model(image, size=resolution)
    n = len(result.xyxy[0].cpu().numpy().tolist())

    if n > 0:
        predictions = result.xyxy[0].cpu().numpy().tolist()[0][-1]
        return predictions, result.render()[0]
    else:
        return -1, image 
        
def most_frequent(prediction_list):
    counter = 0
    num = prediction_list[0]
    for i in prediction_list:
        curr_frequency = prediction_list.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

def main():
    try:
        rospy.init_node('detect_server')
        ## Detection Frequency
        detection_rate = rospy.get_param('~frequency')
        rate = rospy.Rate(detection_rate)

        ## Load Object Detection Model
        model_path = rospy.get_param('~model_path')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)  
        model.conf = 0.4

        ## Camera
        # Camera Display Settings
        dispW = 1280
        dispH = 720
        flip  = 2
        # Camera Capture Settings
        capW = rospy.get_param('~camera/capture_width')
        capH = rospy.get_param('~camera/capture_height')
        fps = rospy.get_param('~camera/fps')
        camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width='+str(capW)+', height='+str(capH)+', format=NV12, framerate='+str(fps)+'/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        cam = cv2.VideoCapture(camSet)

        predictions = []
        n = 0
        while not rospy.is_shutdown():
            ret, frame = cam.read()
            if ret:
                p, img = predict(frame, model, 640)
                predictions.append(p)

            if n == 3:
                n = 0
                predict = most_frequent(predictions)
                predictions.clear()
                print(predict)

            n += 1
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
    finally:
        cam.release()   

if __name__ == '__main__':
    main()
