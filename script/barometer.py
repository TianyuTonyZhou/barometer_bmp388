#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import serial   # dependency: pip install pyserial

import rclpy
from rclpy.node import Node
from barometer_bmp388.msg import Barometer


class BarometerNode(Node):
    def __init__(self):
        super().__init__('barometer_node')

        self.declare_parameter('port', '/dev/mega2560')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('port').get_parameter_value().string_value
        baud = self.get_parameter('baudrate').get_parameter_value().integer_value

        self.publisher = self.create_publisher(Barometer, '/barometer/raw', 1)

        self.get_logger().info(f'Opening {port}...')
        try:
            self.ser = serial.Serial(port=port, baudrate=baud, timeout=5)
        except serial.serialutil.SerialException:
            self.get_logger().error(
                f'Barometer not found at port {port}. Did you specify the correct port?')
            raise


        # Use a timer-driven read loop so rclpy.spin() can also handle shutdown
        self.timer = self.create_timer(0.01, self.read_serial)

    def read_serial(self):
        try:
            line = self.ser.readline().rstrip().decode('utf-8')
            words = line.split(',')
            if len(words) == 3:
                msg = Barometer()
                msg.altitude    = float(words[0])
                msg.pressure    = float(words[1])
                msg.temperature = float(words[2])
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = 'base_link'
                # NOTE: header.seq removed in ROS 2
                self.publisher.publish(msg)
        except Exception:
            return
        

def main(args=None):
    rclpy.init(args=args)
    node = BarometerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.ser.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()