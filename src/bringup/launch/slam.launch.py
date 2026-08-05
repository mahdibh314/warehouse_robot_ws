import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    slam_toolbox_share = get_package_share_directory('slam_toolbox')
    slam_launch_path = os.path.join(slam_toolbox_share, 'launch', 'online_async_launch.py')

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock from Gazebo'
    )

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch_path),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    return LaunchDescription([
        declare_use_sim_time,
        slam
    ])
