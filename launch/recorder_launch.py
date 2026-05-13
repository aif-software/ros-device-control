from launch_ros.actions import Node
from launch import LaunchDescription
import os
import datetime


def generate_launch_description():

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    params_file = os.getenv("RECORDER_QOS_FILE", default="recorder_params.yaml")

    return LaunchDescription(
        [
            Node(
                package="rosbag2_transport",
                executable="recorder",
                name="recorder",
                output="screen",
                parameters=[
                    params_file,
                    {"storage.uri": f"bags/bag_{timestamp}"},
                ],
            )
        ]
    )
