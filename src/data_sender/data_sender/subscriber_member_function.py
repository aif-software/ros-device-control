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
from sensor_msgs.msg import Image


class DataSenderNode(Node):

    def __init__(self):
        super().__init__('data_sender')
        self.create_subscription(
            Image,
            '/flir_refined',
            self.flir_callback,
            1)
        
        self.create_subscription(
            PointCloud2,
            '/lidar_refined',
            self.lidar_callback,
            1)
        

    def flir_callback(self, msg):
        self.get_logger().info('Message in /flir_refined')

    def lidar_callback(self, msg):
        self.get_logger().info('Message in /lidar_refined')

def main(args=None):
    rclpy.init(args=args)

    data_sender = DataSenderNode()

    rclpy.spin(data_sender)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    data_sender.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
