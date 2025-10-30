from functools import partial
import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from sensor_msgs.msg import PointCloud2, Image
from datetime import datetime as time

import rosbag2_py

# I have opted to define this here for some reason.
topics_info = [
    # Lidar
    {
        "name": "/lidar_points",
        "type": PointCloud2,
        "typestring": "sensor_msgs/msg/PointCloud2",
    },
    # Flir
    {
        "name": "/image_raw",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },
    # Stereo camera
    {
        "name": "/aux/image_color",
        "type": Image,
        "typestring": "sensor_msgs/msg/Image",
    },  # Stereo camera data
    {"name": "/left/cost", "type": Image, "typestring": "sensor_msgs/msg/Image"},
    {"name": "/left/depth", "type": Image, "typestring": "sensor_msgs/msg/Image"},
    {"name": "/left/image_rect", "type": Image, "typestring": "sensor_msgs/msg/Image"},
    {"name": "/right/image_rect", "type": Image, "typestring": "sensor_msgs/msg/Image"},
]


# INFO: I don't like python...
class SimpleBagRecorder(Node):
    # Define class constructor
    def __init__(self):
        super().__init__("simple_bag_recorder")
        logger = self.get_logger()
        # Create a writer object for storing data in a bag
        self.writer = rosbag2_py.SequentialWriter()

        # Create timestamp so new bags don't collide
        timestamp = str(time.now()).replace(" ", "_")
        # Define the writer obj options
        storage_options = rosbag2_py.StorageOptions(
            uri=f"bags/{timestamp}", storage_id="mcap"
        )
        converter_options = rosbag2_py.ConverterOptions("", "")
        # Open the bag with writer + defined options
        self.writer.open(storage_options, converter_options)

        # Tell writer necessary info for storing topic data.
        for entry in topics_info:
            # Define topic metadata
            topic_info = rosbag2_py.TopicMetadata(
                id=0,
                name=entry["name"],
                type=entry["typestring"],
                serialization_format="cdr",
            )

            # Create the topic
            self.writer.create_topic(topic_info)

            # Create subscription for the topics the writer needs to listen.
            self.subscription = self.create_subscription(
                entry["type"],
                entry["name"],
                partial(self.data_writing_callback, topic_name=entry["name"]),
                10,
            )
            logger.info(f"Initialized setup for: {entry["name"]}")

    # Define subscription callback for writing data.
    def data_writing_callback(self, msg, topic_name):
        logger = self.get_logger()
        logger.info(f"Topic: {topic_name}")
        self.writer.write(
            topic_name, serialize_message(msg), self.get_clock().now().nanoseconds
        )


def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
