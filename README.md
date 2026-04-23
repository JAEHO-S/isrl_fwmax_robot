# isrl_fwmax_robot

`isrl_fwmax_robot` is a custom ROS 2 package set for the FWMAX Pro robot. It contains three main packages:

- `isrl_robot_description`: robot description, URDF/xacro, and mesh assets
- `isrl_fwmax_nav2`: Nav2 launch configuration and parameters
- `isrl_fwmax_slam`: slam_toolbox launch configuration and parameters

## Packages

- `isrl_robot_description`: provides the FWMAX Pro robot model and mesh
- `isrl_fwmax_nav2`: launches Nav2 with robot-specific navigation parameters
- `isrl_fwmax_slam`: launches slam_toolbox for online SLAM mapping

## Usage

1. Build the workspace:
```bash
cd /home/jhgod/fwmax_ws
colcon build --packages-select isrl_robot_description isrl_fwmax_nav2 isrl_fwmax_slam
```

2. Source the install overlay:
```bash
source install/setup.bash
```

3. Launch Nav2:
```bash
ros2 launch isrl_fwmax_nav2 nav2.launch.py
```

4. Launch SLAM:
```bash
ros2 launch isrl_fwmax_slam slam_toolbox.launch.py
```

5. Launch the robot description:
```bash
ros2 launch isrl_robot_description robot.launch.py
```

## Notes

- `isrl_fwmax_nav2` uses `params/nav2_params2.yaml` and includes an absolute map path at `/home/jhgod/maps/lab_map.yaml`.
- The package launch file loads `maps/lab_map.yaml` from the package, but the Nav2 parameters also reference a map server configuration.
- Sensor topics are configured for Ouster LiDAR (`/ouster/scan`, `/ouster/points`). Adjust topic names as needed for your setup.

## Build type

- `isrl_robot_description`: ament_cmake
- `isrl_fwmax_nav2`: ament_python
- `isrl_fwmax_slam`: ament_python

## Summary

This repository provides the FWMAX Pro robot description, Nav2 navigation stack, and slam_toolbox SLAM stack in a compact ROS 2 package collection.
