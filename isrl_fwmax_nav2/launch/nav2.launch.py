from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    map_file = PathJoinSubstitution([
        FindPackageShare('isrl_fwmax_nav2'),
        'maps',
        'lab_map.yaml'
    ])

    params_file = PathJoinSubstitution([
        FindPackageShare('isrl_fwmax_nav2'),
        'params',
        'nav2_params2.yaml'
    ])

    nav2_launch_file = PathJoinSubstitution([
        FindPackageShare('nav2_bringup'),
        'launch',
        'bringup_launch.py'
    ])

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch_file),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'false',
                'params_file': params_file,
            }.items()
        )
    ])