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
                namespace="flir_1",
                remappings=[("/image_raw", "/flir_1/image_raw")],
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
                namespace="flir_2",
                remappings=[("/image_raw", "/flir_2/image_raw")],
                parameters=[
                    {
                        "output_encoding": "mono16",
                        "pixel_format": "Y16 ",
                        "video_device": "/dev/video2",
                    }
                ],
            ),
            # Stereocamera
            Node(
                name="stereocamera_driver",
                package="multisense_ros",
                executable="ros_driver",
            ),
            # Foxglove bridge
            Node(
                name="foxglove_bridge",
                package="foxglove_bridge",
                executable="foxglove_bridge",
            ),
            # Data sender
            Node(
                name="data_sender",
                package="data_sender",
                executable="talker",
                parameters=[{"mqtt_host": "86.50.228.229"}],
            ),
            # Rosbag
            launch.actions.ExecuteProcess(
                cmd=[
                    "ros2",
                    "bag",
                    "record",
                    "--max-bag-duration",
                    "10",
                    "--compression-mode",
                    "file",
                    "--compression-format",
                    "zstd",
                    "--output",
                    f"bags/{time}",
                    "--topics",
                    "/lidar_points",
                    "/flir_1/image_raw",
                    "/aux/image_color",
                    "/left/cost",
                    "/left/depth",
                    "/left/image_rect",
                    "/right/image_rect",
                    "/flir_2/image_raw",
                    "/lidar_imu",
                ],
                output="screen",
            ),
        ]
    )
