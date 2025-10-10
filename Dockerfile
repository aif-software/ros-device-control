FROM ros:jazzy-ros-core

# setup working directory
WORKDIR /app

# copy source code
COPY src src

# copy launch script
COPY launch/ros_system_launch.py launch.py

# install system dependencies
RUN apt-get update && apt-get install -y \
    libboost-all-dev \
    libyaml-cpp-dev \
    build-essential \
    cmake \
    python3-colcon-common-extensions \
    python3-rosdep

# use bash (because i'm noob)
SHELL ["/bin/bash", "-c"]

# install dependencies and build
# WARNING: docker RUN commands will initialize new shells so source need to be run.
RUN source /opt/ros/jazzy/setup.bash && \
    rosdep init &&  \
    rosdep update && \
    rosdep install --from-paths src -y --ignore-src && \
    colcon build --symlink-install && \
    colcon build --symlink-install # some duct tape here don't mind me

# launch ros package
CMD ["bash", "-c", "source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 launch launch.py"]
