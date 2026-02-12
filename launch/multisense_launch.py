import launch
import datetime as dt

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    time = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")

    return LaunchDescription(
        [
            # Stereocamera
            Node(
                name="stereocamera_driver",
                package="multisense_ros",
                executable="ros_driver",
            ),
            # Foxglove bridge
           # Node(
           #     name="foxglove_bridge",
           #     package="foxglove_bridge",
           #     executable="foxglove_bridge",
           # ),
            # Data sender
           # Node(
           #     name="data_sender",
           #     package="data_sender",
           #     executable="talker",
           # ),
        ]
    )
