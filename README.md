# ros-camera-control

# Setup

Here is the documentation for setting up the repository

## Dependencies

After cloning the repository submodules need to be initialized (HesaiDrivers).

```bash
git submodule update --init --recursive
```

You can also do this while cloning the repository

```bash
git clone --recurse-submodules git@github.com:aif-software/ros-camera-control.git
```

## Stereo Camera

For the stereo camera, we use the ROS2 drivers provided by [Carnegier Robotics](https://github.com/carnegierobotics/multisense_ros2?tab=readme-ov-file).

```bash
ros2 launch multisense_ros multisense_launch.py ip_address:=192.168.88.10
```
