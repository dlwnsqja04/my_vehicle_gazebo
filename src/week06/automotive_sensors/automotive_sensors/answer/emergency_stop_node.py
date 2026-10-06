import math
from typing import Final

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


DEFAULT_FRONT_ANGLE_DEG: Final = 20.0
DEFAULT_STOP_DISTANCE_M: Final = 1.0
RED: Final = '\x1b[31m'
RESET: Final = '\x1b[0m'


def nearest_front_obstacle(
    scan: LaserScan,
    front_half_angle: float = math.radians(DEFAULT_FRONT_ANGLE_DEG),
    stop_distance: float = DEFAULT_STOP_DISTANCE_M,
) -> float | None:
    nearest = None
    for index, distance in enumerate(scan.ranges):
        angle = scan.angle_min + index * scan.angle_increment
        if abs(angle) > front_half_angle:
            continue
        if not math.isfinite(distance) or not scan.range_min <= distance <= scan.range_max:
            continue
        if distance > stop_distance:
            continue
        if nearest is None or distance < nearest:
            nearest = distance
    return nearest


class EmergencyStopNode(Node):
    def __init__(self) -> None:
        super().__init__('emergency_stop_node')
        self.declare_parameter('front_angle_deg', DEFAULT_FRONT_ANGLE_DEG)
        self.declare_parameter('stop_distance_m', DEFAULT_STOP_DISTANCE_M)
        front_angle_deg = float(self.get_parameter('front_angle_deg').value)
        stop_distance_m = float(self.get_parameter('stop_distance_m').value)
        self.front_half_angle = math.radians(front_angle_deg)
        self.stop_distance = stop_distance_m
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data,
        )
        self.stop_state_publisher = self.create_publisher(Bool, '/emergency_stop', 10)

    def scan_callback(self, scan: LaserScan) -> None:
        distance = nearest_front_obstacle(scan, self.front_half_angle, self.stop_distance)
        self.stop_state_publisher.publish(Bool(data=distance is not None))
        if distance is not None:
            self.get_logger().warning(
                f'{RED}[EMERGENCY_STOP] 전방 장애물 감지! 거리: {distance:.2f}m{RESET}',
                throttle_duration_sec=1.0,
            )


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = EmergencyStopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('사용자 인터럽트로 긴급 정지 노드를 종료합니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
