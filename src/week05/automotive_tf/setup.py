from glob import glob
from setuptools import find_packages, setup


package_name = 'automotive_tf'


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
    description='Week 5 TF2 broadcasters and listener',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'static_tf_broadcaster.py = automotive_tf.static_tf_broadcaster:main',
            'dynamic_tf_broadcaster.py = automotive_tf.dynamic_tf_broadcaster:main',
            'tf_listener.py = automotive_tf.tf_listener:main',
        ],
    },
)
