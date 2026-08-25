#!/bin/bash
set -e

source /opt/ros/jazzy/setup.bash

if [ -n "$BAG" ]; then
    echo "Playing bag: $BAG"
    ros2 bag play "/mnt/Burak2/ros-device-control$BAG" &
    BAG_PID=$!
fi

echo "Starting Foxglove bridge..."
ros2 run foxglove_bridge foxglove_bridge

if [ -n "$BAG_PID" ]; then
    wait "$BAG_PID"
fi
