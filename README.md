# Setup the environment  
```bash  
sudo pip3 install rospkg catkin_pkg
sudo pip3 install --upgrade adafruit_blinka
```
## Create the workspace and download the repo
```bash  
mkdir -p ~/catkin_ws/src  
cd ~/catkin_ws/src  
git clone git@github.com:ProfSayed/Jetson.git  
cd ~/catkin_ws/  
catkin_make  
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc  
source ~/.bashrc  
```
Make all python scripts executable in the directory in order to run them  
```bash  
cd ~/catkin_ws/src/Jetson  
find ./ -name *.py -exec chmod +x {} \;
```
# Running the System
## To run the full system  
```bash  
roslaunch jetson_bringup start_bringup.launch  
```
## To run nodes individually  
1. Run roscore
```bash  
roscore  
```
2. In a new Shell: Initialize parameters  
```bash  
roslaunch jetson_bringup param_initializer.launch  
```
Now Run any node as you like:  
* Run Object Detection node  
```rosrun jetson_detection detect_server.py```  
* Run Pusher and Stopper Server  
```roslaunch jetson_bringup start_actuators.launch```  
* You can now Call Stopper and the Pusher (True or False)  
```rosservice call /pusher_action True```  
```rosservice call /stopper_action True```  

