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

from sensor_msgs.msg import PointCloud2, Image


class Logger(Node):

    def __init__(self):
        super().__init__("logger")
        self.create_subscription(
            PointCloud2, "/lidar_points", self.lidar_listener_callback, 10
        )
        self.create_subscription(Image, "/image_raw", self.flir_listener_callback, 10)

    def lidar_listener_callback(self, msg: PointCloud2):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def flir_listener_callback(self, msg: Image):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Logger()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
