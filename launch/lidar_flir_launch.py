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
            # Flir 1
            Node(
                name="flir_driver",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                namespace="flir_left",
                remappings=[('/image_raw', '/flir_left/image_raw')],
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
                name="flir_driver2",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                namespace="flir_right",
                remappings=[('/image_raw', '/flir_right/image_raw')],
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
