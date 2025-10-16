from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="hesai_ros_driver",
                executable="hesai_ros_driver_node",
                name="lidar_driver",
            ),
            Node(
                package="python_lidar_subscriber",
                executable="listener",
                name="lidar_listener",
            ),
            Node(
                package="v4l2_camera",
                executable="v4l2_camera_node",
                name="flir_driver",
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video4",
                    }
                ],
            ),
            Node(
                package="python_flir_subscriber",
                executable="listener",
                name="flir_listener",
            ),
        ]
    )
