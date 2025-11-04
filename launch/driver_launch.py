from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                name="lidar_driver",
                package="hesai_ros_driver",
                executable="hesai_ros_driver_node",
            ),
            Node(
                name="flir_driver",
                package="v4l2_camera",
                executable="v4l2_camera_node",
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video4",
                    }
                ],
            ),
            Node(
                package="multisense_ros",
                executable="ros_driver",
            ),
        ]
    )
