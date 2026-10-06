import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sensor_share = get_package_share_directory('automotive_sensors')
    world_path = os.path.join(sensor_share, 'worlds', 'sensor_track.sdf')
    sensor_bridge = os.path.join(sensor_share, 'config', 'sensor_bridge.yaml')
    clock_bridge = os.path.join(sensor_share, 'config', 'clock_bridge.yaml')
    model_path = os.path.join(sensor_share, 'urdf', 'vehicle_with_sensors.urdf.xacro')
    rviz_config = os.path.join(sensor_share, 'rviz', 'sensors.rviz')
    robot_description = xacro.process_file(model_path).toxml()
    headless = LaunchConfiguration('headless')
    front_angle_deg = LaunchConfiguration('front_angle_deg')
    stop_distance_m = LaunchConfiguration('stop_distance_m')

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_sensor_vehicle',
        output='screen',
        arguments=[
            '-name', 'auto_vehicle', '-string', robot_description,
            '-x', '0.0', '-y', '-4.0', '-z', '0.20',
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('front_angle_deg', default_value='20.0'),
        DeclareLaunchArgument('stop_distance_m', default_value='1.0'),
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
            output='screen',
            condition=UnlessCondition(headless),
        ),
        ExecuteProcess(
            cmd=['gz', 'sim', '-s', '-r', world_path],
            output='screen',
            condition=IfCondition(headless),
        ),
        Node(
            package='ros_gz_bridge', executable='parameter_bridge',
            name='clock_bridge', parameters=[{'config_file': clock_bridge}],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge', executable='parameter_bridge',
            name='sensor_bridge', parameters=[{'config_file': sensor_bridge}],
            output='screen',
        ),
        Node(
            package='robot_state_publisher', executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
            output='screen',
        ),
        Node(
            package='joint_state_publisher', executable='joint_state_publisher',
            parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
            output='screen',
        ),
        TimerAction(period=5.0, actions=[spawn]),
        Node(
            package='automotive_sensors', executable='sensor_listener',
            parameters=[{'use_sim_time': True}], output='screen',
        ),
        Node(
            package='automotive_sensors', executable='emergency_stop_node',
            parameters=[
                {
                    'use_sim_time': True,
                    'front_angle_deg': front_angle_deg,
                    'stop_distance_m': stop_distance_m,
                },
            ],
            additional_env={'RCUTILS_COLORIZED_OUTPUT': '1'}, output='screen',
        ),
        Node(
            package='rviz2', executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            additional_env={'QT_QPA_PLATFORM': 'xcb'},
            condition=UnlessCondition(headless), output='screen',
        ),
    ])
