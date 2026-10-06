import math

import pytest
from sensor_msgs.msg import LaserScan

from automotive_sensors.answer.emergency_stop_node import nearest_front_obstacle


def make_scan(ranges: list[float], angle_min: float, angle_increment: float) -> LaserScan:
    scan = LaserScan()
    scan.ranges = ranges
    scan.angle_min = angle_min
    scan.angle_increment = angle_increment
    scan.range_min = 0.15
    scan.range_max = 20.0
    return scan


def test_detects_obstacle_at_front_angle_and_distance_boundaries() -> None:
    scan = make_scan([1.0, math.inf, 1.0], -math.radians(20), math.radians(20))

    result = nearest_front_obstacle(scan)

    assert result == 1.0


def test_ignores_closer_obstacle_outside_front_sector() -> None:
    scan = make_scan([0.2, 0.7, 0.2], -math.radians(30), math.radians(30))

    result = nearest_front_obstacle(scan)

    assert result == pytest.approx(0.7)


def test_ignores_invalid_ranges_and_returns_none_without_front_obstacle() -> None:
    scan = make_scan([math.nan, math.inf, 0.1, 1.1], -math.radians(15), math.radians(10))

    result = nearest_front_obstacle(scan)

    assert result is None


def test_uses_runtime_angle_and_distance_parameters() -> None:
    scan = make_scan([0.6, 0.8, 0.6], -math.radians(30), math.radians(30))

    result = nearest_front_obstacle(
        scan,
        front_half_angle=math.radians(10),
        stop_distance=0.7,
    )

    assert result is None
