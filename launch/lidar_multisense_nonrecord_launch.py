import launch
import datetime as dt

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    time = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")

    return LaunchDescription(
        [
            # Lidar
            Node(
                name="lidar_driver",
                package="hesai_ros_driver",
                executable="hesai_ros_driver_node",
            ),
            # Stereocamera
            Node(
                name="stereocamera_driver",
                package="multisense_ros",
                executable="ros_driver",
            ),
            # Data sender
           # Node(
           #     name="data_sender",
           #     package="data_sender",
           #     executable="talker",
           # ),
        ]
    )
