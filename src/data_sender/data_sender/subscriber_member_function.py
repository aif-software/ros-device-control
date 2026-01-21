# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2

import paho.mqtt.client as mqtt

import json
import zlib


class DataSenderNode(Node):

    def __init__(self):
        super().__init__("data_sender")
        self.get_logger().info("Initializing DataSenderNode...")

        # Declare parameters
        self.declare_parameter("mqtt_host", "localhost")

        # Create callbackgroup
        self.subscription_callbackgroup = ReentrantCallbackGroup()

        # Create Pointcloud2 subscription handler
        self.create_subscription(
            msg_type=PointCloud2,
            topic="/lidar_points",
            callback=self.send_pointcloud2,
            qos_profile=1,
            callback_group=self.subscription_callbackgroup,
        )

        # Create mqtt client
        self.mqtt_client = mqtt.Client()
        # Connect to broker
        self.mqtt_client.connect(
            self.get_parameter("mqtt_host").get_parameter_value().string_value
        )
        # Start network loop
        self.mqtt_client.loop_start()

        self.get_logger().info("DataSenderNode initialized.")

    def send_pointcloud2(self, msg: PointCloud2):
        try:
            header = {
                "stamp": {
                    "sec": msg.header.stamp.sec,
                    "nanosec": msg.header.stamp.nanosec,
                },
            }

            fields = [
                {
                    "name": f.name,
                    "offset": f.offset,
                    "datatype": f.datatype,
                    "count": f.count,
                }
                for f in msg.fields
            ]

            metadata = {
                "header": header,
                "height": msg.height,
                "width": msg.width,
                "fields": fields,
                "is_bigendian": msg.is_bigendian,
                "point_step": msg.point_step,
                "row_step": msg.row_step,
                "is_dense": msg.is_dense,
            }

            # Compress with zlib
            compressed_data = zlib.compress(msg.data)

            # Send the data to MQTT
            self.get_logger().info("Publishing data to MQTT...")
            self.mqtt_client.publish(
                "pointcloud2/metadata",
                json.dumps(metadata),
                qos=0,
            )
            self.mqtt_client.publish(
                "pointcloud2/data",
                compressed_data,
                qos=0,
            )
        except Exception as e:
            self.get_logger().info(f"MQTT publish failed: {e}")


def main(args=None):
    rclpy.init(args=args)

    node = DataSenderNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        node.get_logger().info("Starting DataSenderNode...")
        executor.spin()
    except KeyboardInterrupt:
        return

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
