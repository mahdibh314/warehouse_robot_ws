from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    dashboard_node = Node(
        package='dashboard',
        executable='dashboard_node',
        name='dashboard_node',
        output='screen'
    )

    return LaunchDescription([
        dashboard_node
    ])
