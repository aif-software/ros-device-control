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
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2

import paho.mqtt.client as mqtt

import json
import zlib
import base64


class DataSenderNode(Node):

    def __init__(self):
        super().__init__("data_sender")
        self.get_logger().info("Initializing DataSenderNode...")

        # Declare parameters
        self.declare_parameter("mqtt_host", "localhost")

        # Create mqtt client
        self.mqtt_client = mqtt.Client()

        # Connect to broker
        self.mqtt_client.connect(
            self.get_parameter("mqtt_host").get_parameter_value().string_value
        )
        # Start network loop
        self.mqtt_client.loop_start()

        # Maximum number of messages that can be partway through the network (QoS > 0).
        self.mqtt_client.max_inflight_messages_set(1)

        # Maximum number of outgoing messages in queue.
        self.mqtt_client.max_queued_messages_set(1)

        # Setup the qos profile
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        # Create Pointcloud2 subscription handler
        self.create_subscription(
            msg_type=PointCloud2,
            topic="/lidar_points",
            callback=self.send_data,
            qos_profile=qos,
        )

        self.get_logger().info("DataSenderNode initialized.")

    def send_data(self, msg: PointCloud2):
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

        # Compress with zlib
        compressed_data = zlib.compress(msg.data)

        # Encode into base64 and turn into ascii string
        string_data = base64.b64encode(compressed_data).decode("ascii")

        payload = {
            "header": header,
            "height": msg.height,
            "width": msg.width,
            "fields": fields,
            "is_bigendian": msg.is_bigendian,
            "point_step": msg.point_step,
            "row_step": msg.row_step,
            "is_dense": msg.is_dense,
            "data": string_data,
        }

        try:
            # Send the data to MQTT
            info = self.mqtt_client.publish("ros2/lidar", json.dumps(payload), qos=1)
            if info.rc == 0:
                self.get_logger().info(
                    f"New message queued mid: {info.mid}, header: {header}"
                )
        except Exception as e:
            self.get_logger().info(f"MQTT publish failed: {e}")


def main(args=None):
    rclpy.init(args=args)

    node = DataSenderNode()

    try:
        node.get_logger().info("Starting DataSenderNode...")
        rclpy.spin(node)
    except KeyboardInterrupt:
        return

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
