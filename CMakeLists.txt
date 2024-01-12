cmake_minimum_required(VERSION 3.0.2)
project(joint_state_publisher_gui)

find_package(catkin REQUIRED COMPONENTS rospy roscpp std_msgs sensor_msgs)

catkin_package()

catkin_install_python(PROGRAMS scripts/joint_state_publisher_gui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
