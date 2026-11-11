from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            # Lidar
            Node(
                name="imu_driver",
                package="bosch_imu",
                executable="bosch_node",
            ),
        ]
    )
