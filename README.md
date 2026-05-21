# ros-device-control

## Dependencies

```bash
# Do not care if this says you have already created it, its okay.
rosdep init

# Update
rosdep update

# Install package dependencies (Must be run in the ROOT folder).
rosdep install --from-paths src -y --ignore-src
```

## Building

```bash
# This must be run in the ROOT directory
colcon build
```

## Running

The package names can be found in src/<project-folder>/package.xml.
There is a line called "name" which tells the name of the specific package.

This is not to be confused with the folder name which can be whatever.
Only name that matters is the name in the package.xml.

Ros run will autocorrect the package names so they don't always need to be fully typed.

```bash
ros2 run <package-name> <node-name>
```

## Docker

Easy to setup just build the image from Dockerfile and run.

The run command displayed here will use the host computers network
and forward the device /dev/video0 to the container and its name will be
/dev/video4 inside the container. Both of these names can be changed depending
on where the device actually lands on your computer.

```bash
# Build image
docker build -t ros-devices .

# Run container (in the repository root!)
docker run --device=/dev/video0:/dev/video4 --device=/dev/video2:/dev/video6 --volume /mnt/burak2/ros-device-control/bags:/app/bags --network=host -d ros-devices:latest
```

### Optional

To help finding video devices install video4linux utilities.

```bash
sudo apt install v4l-utils
```

If you are on a distro that doesn't use apt find the corresponding package by yourself.
This package for example is on the arch repo with the same name.

After installing the utilities you can find cameras with

```bash
v4l2-ctl --list-devices
```

## ROS node architecture

```mermaid
classDiagram
class DeviceNode{
 topic[]
}
class SubscriberNode{
 subscription
 refinedDataTopic
 refineDataToDesiredForm()
}
class DataSenderNode{
 subscriptions[]
 sendDataToCloud()
 saveDataLocally()
}
class Logger{
subscriptions[]
whenLastMessageFromSubscription[]
printToTerminal()
}
 DeviceNode "1" --> "1" SubscriberNode
 SubscriberNode "*" --> "1" DataSenderNode
 SubscriberNode "*" --> "1" Logger
```

## Other related repositories
- [UI](https://github.com/M3S-Kuura/Ros2-recording-UI)
- [Bag processor](https://github.com/M3S-Kuura/Ros2-bag-processsor)
