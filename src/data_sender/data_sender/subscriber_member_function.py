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
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2

import paho.mqtt.client as mqtt

import json


class DataSenderNode(Node):

    def __init__(self):
        super().__init__("data_sender")
        self.get_logger().info("initializing data sender...")

        # Create Pointcloud2 subscription handler
        self.create_subscription(
            msg_type=PointCloud2,
            topic="/lidar_points",
            callback=self.pointcloud2_sender_callback,
            qos_profile=1,
        )

        # Create mqtt client connection
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("86.50.228.229")
        self.mqtt_client.loop_start()

        self.get_logger().info("data sender initialized.")

    # Pointcloud2 callback
    def pointcloud2_sender_callback(self, msg: PointCloud2):
        header = {
            "stamp": {
                "sec": msg.header.stamp.sec,
                "nanosec": msg.header.stamp.nanosec,
            },
            "frame_id": msg.header.frame_id,
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

        # TODO: optimize
        payload = {
            "header": header,
            "height": msg.height,
            "width": msg.width,
            "fields": fields,
            "is_bigendian": msg.is_bigendian,
            "point_step": msg.point_step,
            "row_step": msg.row_step,
            "is_dense": msg.is_dense,
            "data": [int(x) for x in msg.data],
        }

        self.mqtt_client.publish("test/lidar", json.dumps(payload))


def main(args=None):
    rclpy.init(args=args)

    data_sender = DataSenderNode()

    rclpy.spin(data_sender)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    data_sender.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
