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
## FLIR-Camera
For the Flir-camera we currently use [v4l2-camera](https://gitlab.com/boldhearts/ros2_v4l2_camera) library.
```bash
ros2 run v4l2_camera v4l2_camera_node --ros-args --params-file v4l2_camera/v4l2_params.yaml
```
