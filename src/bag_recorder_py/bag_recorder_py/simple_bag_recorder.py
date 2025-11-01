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
        self.logger = self.get_logger()
        # Create a writer object for storing data in a bag

        # Define timestamp and various options
        timestamp = str(time.now()).replace(" ", "_")
        storage_options = rosbag2_py.StorageOptions(
          uri=f"bags/{timestamp}",
          storage_id="mcap",
          max_bagfile_duration=10
        )
        compression_options = rosbag2_py.CompressionOptions()
        compression_options.compression_format = 'zstd'
        compression_options.compression_mode = rosbag2_py.CompressionMode.FILE

        converter_options = rosbag2_py.ConverterOptions("", "")

        # define other topics in a for loop when needed
        topic_metadata = rosbag2_py.TopicMetadata(
            id=0,
            name='/lidar_points',
            type='sensor_msgs/msg/PointCloud2',
            serialization_format='cdr'
        )

        # Create writer instance with CompressionOptions
        self.writer = rosbag2_py.SequentialCompressionWriter(compression_options)
        self.writer.open(storage_options, converter_options)
        self.writer.create_topic(topic_metadata)
        
        # Currently only subscribes to /lidar_points. flirs should be added for poc
        self.sub = self.create_subscription(PointCloud2, '/lidar_points', self.topic_callback, 10)

    # dis bad hardcoding sory
    def topic_callback(self, msg):
        self.writer.write(
            '/lidar_points',
            serialize_message(msg),
            self.get_clock().now().nanoseconds
        )

def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
