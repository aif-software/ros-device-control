# ros-camera-control

## FLIR-Camera
For the Flir-camera we currently use [v4l2-camera](https://gitlab.com/boldhearts/ros2_v4l2_camera) library.

To run the camera node
```bash
# Do not care if this says you have already created it, its okay.
rosdep init

# Update 
rosdep update

# Install package dependencies (Must be run in the ROOT folder).
rosdep install --from-paths src -y --ignore-src
```
