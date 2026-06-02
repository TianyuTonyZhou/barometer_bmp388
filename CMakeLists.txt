cmake_minimum_required(VERSION 3.14)
project(barometer_bmp388)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rclpy REQUIRED)

# Generate the message
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Barometer.msg"
  DEPENDENCIES std_msgs
)

# Install Python script as an executable
install(PROGRAMS
  script/barometer.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()