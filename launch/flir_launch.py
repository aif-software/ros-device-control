from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            # Flir 1
            Node(
                name="flir_driver",
                package="v4l2_camera",
                namespace="flir_left",
                remappings=[("/image_raw", "/flir_left/image_raw")],
                executable="v4l2_camera_node",
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
                namespace="flir_right",
                remappings=[("/image_raw", "/flir_right/image_raw")],
                executable="v4l2_camera_node",
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
