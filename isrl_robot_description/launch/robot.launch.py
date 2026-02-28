import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Get package share directory
    isrl_robot_desc_share = FindPackageShare('isrl_robot_description')
    
    # Robot Description from xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution(
                [FindPackageShare('xacro'), 'bin', 'xacro']
            ),
            ' ',
            PathJoinSubstitution(
                [isrl_robot_desc_share, 'urdf', 'robot.xacro']
            ),
        ]
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='base_robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description_content},
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
    )

    # Static Transform Publisher: mobile_base_link -> base_0
    static_tf_mobile_base_to_m0609 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='mobile_base_to_m0609',
        arguments=['0.15', '0.0', '0.50', '-1.57', '0.0', '0.0',
                   'mobile_base_link', 'base_0'],
        output='screen',
    )

    # Static Transform Publisher: mobile_base_link -> os_sensor
    static_tf_mobilebase_to_os_sensor = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='mobilebase_to_os_sensor',
        arguments=['0.32', '0.0', '0.36', '0.0', '0.0', '0.0',
                   'mobile_base_link', 'os_sensor'],
        output='screen',
    )

    # Static Transform Publisher: link_6 -> camera_link
    static_tf_link6_to_d455f = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='link6_to_d455f',
        arguments=['-0.07', '0.0', '-0.04', '3.14', '-1.57', '0.0',
                   'link6', 'camera_link'],
        output='screen',
    )

    # yhs_can_control_node
    yhs_can_control_node = Node(
        package='yhs_can_control',
        executable='yhs_can_control_node',
        name='yhs_can_control_node',
        output='screen',
        namespace='mobile_robot',
    )

    # Group all nodes under mobile_robot namespace
    mobile_robot_group = GroupAction(
        actions=[
            robot_state_publisher_node,
            static_tf_mobile_base_to_m0609,
            static_tf_mobilebase_to_os_sensor,
            static_tf_link6_to_d455f,
            yhs_can_control_node,
        ],
        scoped=True,
        launch_configurations={'use_sim_time': LaunchConfiguration('use_sim_time')},
    )

    return LaunchDescription([
        use_sim_time,
        mobile_robot_group,
    ])
