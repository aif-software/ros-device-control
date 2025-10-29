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
from datetime import datetime as dt


# TODO: REFACTOR THIS!
class Logger(Node):

    def __init__(self):
        # Call super constructor
        super().__init__("logger")

        # Create datastruct
        self.logging_data = {
            "lidar": {"count": 0, "lmt": None, "dtime": None},
            "flir": {"count": 0, "lmt": None, "dtime": None},
            "stereo_camera": {"count": 0, "lmt": None, "dtime": None},
        }

        # Create subscription handlers
        self.create_subscription(
            PointCloud2, "/lidar_points", self.lidar_listener_callback, 1
        )
        self.create_subscription(
            Image, "/aux/image_mono", self.multisense_listener_callback, 1
        )
        self.create_subscription(Image, "/image_raw", self.flir_listener_callback, 1)

        # Create timer handler
        self.create_timer(10, self.timer_callback)

    # TODO: Combine these listeners into 1.
    def lidar_listener_callback(self, msg: PointCloud2):
        if msg:
            self.logging_data["lidar"]["count"] += 1
            self.logging_data["lidar"]["lmt"] = dt.now()
            self.logging_data["lidar"]["dtime"] = msg.header.stamp

    def flir_listener_callback(self, msg: Image):
        if msg:
            self.logging_data["flir"]["count"] += 1
            self.logging_data["flir"]["lmt"] = dt.now()
            self.logging_data["flir"]["dtime"] = msg.header.stamp

    def multisense_listener_callback(self, msg: Image):
        if msg:
            self.logging_data["stereo_camera"]["count"] += 1
            self.logging_data["stereo_camera"]["lmt"] = dt.now()
            self.logging_data["stereo_camera"]["dtime"] = msg.header.stamp

    def timer_callback(self):
        logger = self.get_logger()
        for key in self.logging_data:
            count = self.logging_data[key]["count"]
            ltime = self.logging_data[key]["lmt"]
            dtime = self.logging_data[key]["dtime"]
            delta = dt.now() - ltime
            log_string = (
                f"Device: {key}\n"
                f"Message count: {count}\n"
                f"Time since last message: {delta}\n"
                f"Last message time: {ltime}\n"
                f"Device time: {dtime}"
            )
            logger.info(log_string)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Logger()

    rclpy.spin(minimal_subscriber)

    # Excplicitly destroy the node. It will also be GC:d if not destroyed here.
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
