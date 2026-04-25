import os
from ament_index_python import get_package_share_directory
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
    
    # Robot Description from xacro (robot1.xacro for no_arm variant)
    # Use the `xacro` executable from the system PATH (typical location: /opt/ros/<distro>/bin/xacro)
    # Avoid using FindPackageShare('xacro') + 'bin' since that path may not exist.
    # Ensure a space separates the `xacro` executable and the file path so
    # Command concatenation produces a valid command string.
    robot_description_content = Command(
        [
            'xacro',
            ' ',
            PathJoinSubstitution(
                [isrl_robot_desc_share, 'urdf', 'robot1.xacro']
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
        remappings=[
            ('/robot_description', '/mobile_robot_description'),
        ],
    )

    # Static Transform Publisher: base_footprint -> base_link
    static_tf_basefootprint_to_baselink = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='basefootprint_to_baselink',
        arguments=['0.0', '0.0', '0.388', '0.0', '0.0', '0.0',
                   'base_footprint', 'base_link'],
        output='screen',
    )

    # Static Transform Publisher: mobile_base_link -> os_sensor
    static_tf_mobilebase_to_os_sensor = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_os_sensor',
        arguments=['0.32', '0.0', '0.505', '0.0', '0.0', '0.0',
                   'base_link', 'os_sensor'],
        output='screen',
    )

    # Static Transform Publisher: mobile_base_link -> IMU sensor
    static_tf_mobilebase_to_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_imu',
        arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0',
                   'base_link', 'imu'],
        output='screen',
    )

    # Static Transform Publisher: mobile_base_link -> camera_link
    static_tf_mobilebase_to_realsense = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_realsense',
        arguments=['0.41', '0.01', '0.335', '0.0', '0.7854', '0.0',
                   'base_link', 'camera_link'],
        output='screen',
    )

    # FWMax CAN Control Node
    share_dir = get_package_share_directory('yhs_can_control')
    parameter_file = LaunchConfiguration('params_file')

    params_declare = DeclareLaunchArgument('params_file',
                                           default_value=os.path.join(
                                               share_dir, 'params', 'cfg.yaml'),
                                           description='FPath to the ROS2 parameters file to use.')

    yhs_can_control_node = Node(package='yhs_can_control',
                                executable='yhs_can_control_node',
                                name='yhs_can_control_node',
                                output='screen',
                                parameters=[parameter_file]
                                )

    # Group all nodes under mobile_robot namespace
    mobile_robot_group = GroupAction(
        actions=[
            robot_state_publisher_node,
            static_tf_basefootprint_to_baselink,
            static_tf_mobilebase_to_os_sensor,
            static_tf_mobilebase_to_imu,
            static_tf_mobilebase_to_realsense,
            params_declare,
            yhs_can_control_node,
        ],
        scoped=True,
        launch_configurations={'use_sim_time': LaunchConfiguration('use_sim_time')},
    )

    return LaunchDescription([
        use_sim_time,
        mobile_robot_group,
    ])
