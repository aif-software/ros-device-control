# Info

The root folder of this document holds all the launch files that
can be used while developing or in production.

Launch files don't start automatically recording a rosbag unless
the file name contains "record".

The intended way to start recording is to run the ros command in a container.
## Device specific launch files

orin_launch.py and nano_launch.py might be copies of other launch files,
but exist just to make it easier to parse which launch files are intended
for the current setup.

As of 12.3.26, orin_launch.py and nano_launch.py are up to date.

## Misc

If you need to run any driver by itself just use the `ros2 run` command
it is sufficient for that kind of purpose. The launch files are here just
so that nobody needs to repeat those commands in million different terminals.
