#!/bin/bash

# Set domain id
export ROS_DOMAIN_ID=42

# Source ros2 executables
source "$ROS2_SOURCE_PATH"/setup.bash

# Source project executables
source "$ROS2_PROJECT_PATH"/install/local_setup.bash

# Run ros2 nodes
ros2 launch ./launch/ros_system_launch.py
