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
from rclpy_message_converter import json_message_converter as jmc

from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image

from queue import Queue
import threading

import paho.mqtt.client as mqtt
import json

topic_info = [
    {
        "device": "flir",
        "topic": "/image_raw",
        "type": Image,
    },
    {
        "device": "stereocamera",
        "topic": "/aux/image_mono",
        "type": Image,
    },
    {
        "device": "lidar",
        "topic": "/lidar_points",
        "type": PointCloud2,
    },
]


# TODO: Compress the topic messages.
class DataSenderNode(Node):

    def __init__(self):
        super().__init__("data_sender")
        self.get_logger().info("initializing data sender...")

        # Create queue for storing data before sending
        self.queue = Queue()

        # Create subscriptions for devices
        for info in topic_info:
            self.create_subscription(
                msg_type=info["type"],
                topic=info["topic"],
                callback=self.subscription_callback,
                qos_profile=1,
            )

        # Create timer for flushing the queue
        self.create_timer(10, self.flush_queue)

        # Create mqtt client connection
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("86.50.228.229")
        self.mqtt_client.loop_start()

        self.get_logger().info("data sender initialized.")

    # Subscriber callback (Everybody uses the same function).
    def subscription_callback(self, msg):
        payload = jmc.convert_ros_message_to_json(msg)
        self.queue.put(payload)

    def send_data(self, batch):
        for msg in batch:
            self.mqtt_client.publish("ros2/sensors", msg)

    # WARN: I'm not sure does the whole flush_queue function block the
    # subscriber threads and if it does the threading needs to be moved one-level up.
    def flush_queue(self):
        self.get_logger().info("flushing queue...")

        # List which is to be sent to the receiver
        batch = []

        # This is now restricted because some devices send a lot of data.
        while not self.queue.empty() and len(batch) <= 1000:
            batch.append(self.queue.get())

        # Only start thread on non-empty batches.
        if batch:
            # This is done with threading because we don't want the timer
            # blocking any resources in case the sending takes a lot of time.
            self.get_logger().info("starting thread")
            threading.Thread(target=self.send_data, args=(batch,), daemon=True).start()

        self.get_logger().info("flushing done.")


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
