from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="hesai_ros_driver",
                namespace="ros_control",
                executable="hesai_ros_driver_node",
                name="lidar_driver",
            ),
            Node(
                package="python_lidar_subscriber",
                namespace="ros_control",
                executable="listener",
                name="lidar_listener",
            ),
        ]
    )
