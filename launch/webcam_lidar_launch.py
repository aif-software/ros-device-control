import launch
import datetime as dt

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    time = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")

    return LaunchDescription(
        [
            # Webcam
            Node(
                name="webcam_driver",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                namespace="webcam",
                remappings=[('/image_raw', '/webcam/image_raw')],
                parameters=[
                    {
                        "video_device": "/dev/video0",
                    }
                ],
            ),
            # Lidar
            Node(
                name="lidar_driver",
                package="hesai_ros_driver",
                executable="hesai_ros_driver_node",
            ),
        ]
    )

