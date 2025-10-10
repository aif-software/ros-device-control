# ros-camera-control

# Setup
Here is the documentation for setting up the repository

## Dependencies
After cloning the repository submodules need to be initialized (HesaiDrivers).

```bash
# Do not care if this says you have already created it, its okay.
rosdep init

# Update 
rosdep update

# Install package dependencies (Must be run in the ROOT folder).
rosdep install --from-paths src -y --ignore-src
```
