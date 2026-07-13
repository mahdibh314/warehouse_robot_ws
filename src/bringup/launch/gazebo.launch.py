import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():

    bringup_share = get_package_share_directory('bringup')
    world_path = os.path.join(bringup_share, 'worlds', 'warehouse.world')

    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    gz_launch_path = os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={'gz_args': world_path}.items()
    )

    description_share = get_package_share_directory('warehouse_robot_description')
    xacro_path = os.path.join(description_share, 'urdf', 'warehouse_robot.urdf.xacro')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    spawn_robot_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'warehouse_robot',
            '-z', '0.1'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_robot_node
    ])
