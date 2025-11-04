from functools import partial
import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from datetime import datetime as time

import rosbag2_py
from topics_info import info


# INFO: I don't like python...
class SimpleBagRecorder(Node):
    # Define class constructor
    def __init__(self):
        super().__init__("simple_bag_recorder")

        # Get the node logger
        logger = self.get_logger()

        # Create timestamp so new bags don't collide
        timestamp = str(time.now()).replace(" ", "_")

        # Storage options
        storage_options = rosbag2_py.StorageOptions(
            uri=f"bags/{timestamp}",
            storage_id="mcap",
            max_bagfile_duration=10,
        )

        # Setup compression options
        compression_options = rosbag2_py.CompressionOptions(
            compression_format="zstd",
            compression_mode=rosbag2_py.CompressionMode.FILE,
        )

        # Setup converter options
        converter_options = rosbag2_py.ConverterOptions("", "")

        # Create a writer object for storing data in a bag
        self.writer = rosbag2_py.SequentialCompressionWriter(compression_options)

        # Open/Create the bag with the writer
        self.writer.open(storage_options, converter_options)

        # Tell writer necessary info for storing topic data.
        for entry in info:
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
                partial(
                    self.data_writing_callback,
                    topic_name=entry["name"],
                ),
                10,
            )
            logger.info(f"Initialized setup for: {entry["name"]}")

    # Define subscription callback for writing data.
    def data_writing_callback(self, msg, topic_name):
        self.writer.write(
            topic_name,
            str(serialize_message(msg)),
            self.get_clock().now().nanoseconds,
        )


def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
