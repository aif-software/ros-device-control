from launch_ros.actions import Node
from launch import LaunchDescription
import datetime

def generate_launch_description():

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    return LaunchDescription([
        Node(
            package='rosbag2_transport',
            executable='recorder',
            name='recorder',
            output="screen",
            parameters=[
                'recorder_params.yaml',
                {
                    "storage.uri": f"bags/bag_{timestamp}"
                }
            ],
        )
    ])
