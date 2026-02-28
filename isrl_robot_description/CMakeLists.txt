cmake_minimum_required(VERSION 3.16)
project(isrl_robot_description)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Configure ROS2 build tools
find_package(ament_cmake REQUIRED)

# Install directory structure for a description package
# Install URDF and Xacro files
install(DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf)

# Install launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch)

# Install mesh files
install(DIRECTORY meshes/
  DESTINATION share/${PROJECT_NAME}/meshes)

# Install RViz files
install(DIRECTORY rviz/
  DESTINATION share/${PROJECT_NAME}/rviz)

ament_package()
