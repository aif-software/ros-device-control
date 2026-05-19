import launch
import datetime as dt

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    time = str(dt.datetime.now()).replace(" ", "_").replace(":", "-")

    return LaunchDescription(
        [
            # Flir 1
            Node(
                name="flir_driver_0",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                namespace="flir_0",
                remappings=[("/image_raw", "/flir_0/image_raw")],
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video0",
                    }
                ],
            ),
            # Flir 2
            Node(
                name="flir_driver_1",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                namespace="flir_1",
                remappings=[("/image_raw", "/flir_1/image_raw")],
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video2",
                    }
                ],
            ),
        ]
    )
