import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    bringup_share = get_package_share_directory('bringup')

    gazebo_launch_path = os.path.join(bringup_share, 'launch', 'gazebo.launch.py')
    dashboard_launch_path = os.path.join(bringup_share, 'launch', 'dashboard.launch.py')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path)
    )

    dashboard = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(dashboard_launch_path)
    )

    return LaunchDescription([
        gazebo,
        dashboard
    ])
