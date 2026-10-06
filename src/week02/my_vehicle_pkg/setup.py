from glob import glob
from setuptools import find_packages, setup


package_name = 'my_vehicle_pkg'


setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dlwnsqja04',
    maintainer_email='dlwnsqja04@users.noreply.github.com',
    description='Week 2 ROS 2 topic communication practice',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'simple_publisher = my_vehicle_pkg.simple_publisher:main',
            'simple_subscriber = my_vehicle_pkg.simple_subscriber:main',
        ],
    },
)
