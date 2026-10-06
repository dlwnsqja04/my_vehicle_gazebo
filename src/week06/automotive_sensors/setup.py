from glob import glob
from setuptools import find_packages, setup


package_name = 'automotive_sensors'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/urdf', glob('urdf/*.xacro')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dlwnsqja04',
    maintainer_email='dlwnsqja04@users.noreply.github.com',
    description='Week 6 Gazebo sensor simulation and emergency warning',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'sensor_listener = automotive_sensors.sensor_listener:main',
            'emergency_stop_node = automotive_sensors.answer.emergency_stop_node:main',
        ],
    },
)
