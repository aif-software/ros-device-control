from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            # Flir 1
            Node(
                name="flir_driver",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video1",
                    }
                ],
            ),
            # Flir 2
            Node(
                name="flir_driver2",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video3",
                    }
                ],
            ),
        ]
    )
