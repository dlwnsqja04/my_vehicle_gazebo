# my_vehicle_gazebo

오토모티브SW프로그래밍 3주차(code03) + 4주차(code04) 통합 ROS 2 패키지입니다.

## 포함 내용
- URDF/Xacro 차량 모델
- RViz2 표시 런치
- Gazebo Sim 트랙 월드
- ros_gz_bridge 설정
- Gazebo 차량 스폰/주행 런치

## 빌드
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_vehicle_gazebo
source install/setup.bash
```

## 3주차 RViz 확인
```bash
ros2 launch my_vehicle_gazebo display.launch.py
```

## 4주차 Gazebo 실행
```bash
ros2 launch my_vehicle_gazebo spawn_car.launch.py
```

다른 터미널에서:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

오도메트리 확인:
```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /odom
```

시뮬레이션 시계 확인:
```bash
ros2 topic hz /clock
```
