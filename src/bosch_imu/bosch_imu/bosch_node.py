import threading
import math
import serial

import rclpy
from rclpy.node import Node
from rclpy.utilities import try_shutdown

from sensor_msgs.msg import Imu, MagneticField


class BoschNode(Node):

    def __init__(self):
        super().__init__("imu_node")
        self.imu_pub = self.create_publisher(Imu, "/bosch/imu", 10)
        self.mag_pub = self.create_publisher(MagneticField, "/bosch/mag", 10)
        self.ser_ = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        self.running = True
        self.serial_thread = threading.Thread(
            target=self.serial_reader_callback, daemon=True
        )
        self.serial_thread.start()

    def serial_reader_callback(self):
        while self.running:
            try:
                data = self.ser_.readline().decode("utf-8").strip()

                if not data:
                    continue

                values = [float(x.strip()) for x in data.split(",")]

                if len(values) != 10:
                    continue

                # Acceleration: mg -> m/s²
                acc_x = values[0] * 9.80665 / 1000.0
                acc_y = values[1] * 9.80665 / 1000.0
                acc_z = values[2] * 9.80665 / 1000.0

                # Gyroscope: mDeg/s -> rad/s
                gyro_x = values[7] * math.pi / 180000.0
                gyro_y = values[8] * math.pi / 180000.0
                gyro_z = values[9] * math.pi / 180000.0

                # Magnetometer: µT -> T
                mag_x = values[3] * 1e-6
                mag_y = values[4] * 1e-6
                mag_z = values[5] * 1e-6

                # IMU message
                imu_msg = Imu()

                imu_msg.header.stamp = self.get_clock().now().to_msg()
                imu_msg.header.frame_id = "imu_link"

                imu_msg.linear_acceleration.x = acc_x
                imu_msg.linear_acceleration.y = acc_y
                imu_msg.linear_acceleration.z = acc_z

                imu_msg.angular_velocity.x = gyro_x
                imu_msg.angular_velocity.y = gyro_y
                imu_msg.angular_velocity.z = gyro_z

                # Orientation unavailable
                imu_msg.orientation_covariance[0] = -1.0

                if not self.context.ok():
                    break

                self.imu_pub.publish(imu_msg)

                # Magnetometer message
                mag_msg = MagneticField()

                mag_msg.header = imu_msg.header

                mag_msg.magnetic_field.x = mag_x
                mag_msg.magnetic_field.y = mag_y
                mag_msg.magnetic_field.z = mag_z

                self.mag_pub.publish(mag_msg)

            except (ValueError, IndexError) as e:
                self.get_logger().warning(f"Invalid serial data: {e}")

            except serial.SerialException as e:
                self.get_logger().error(f"Serial error: {e}")
                break

    def destroy_node(self):
        super().destroy_node()

        self.running = False

        if self.serial_thread.is_alive():
            self.serial_thread.join(timeout=2.0)

        if self.ser_.is_open:
            self.ser_.close()


def main(args=None):
    rclpy.init(args=args)
    node = BoschNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        try_shutdown()


if __name__ == "__main__":
    main()
