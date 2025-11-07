# Info

The root folder of this document holds all the launch files that
can be used while developing or in production.

## Full system

file: full_system_launch.py.

description: Will startup the whole system including all the different
sensor/device drivers and our own custom nodes which handle
the data coming from these devices etc...

purpose: Will be ran on the jetson in containarized environment and does
basically everything needed for the project.

## Device drivers

file: driver_launch.py

description: Will only start all the device/sensor drivers which include
Lidar, Flir(s) and the stereo camera.

purpose: Used for debugging and development for example if someone wants
to add more nodes to the system or test out some functionality you don't
have to run all the nodes.

## Misc

If you need to run any driver by itself just use the `ros2 run` command
it is sufficient for that kind of purpose. The launch files are here just
so that nobody needs to repeat those commands in million different terminals.
