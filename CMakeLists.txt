cmake_minimum_required(VERSION 2.8.3)
# project(teleop_twist_keyboard)
get_filename_component(projname ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" projname ${projname})
project(${projname})

find_package(catkin REQUIRED)

catkin_package()

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS
   teleop_twist_keyboard.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
