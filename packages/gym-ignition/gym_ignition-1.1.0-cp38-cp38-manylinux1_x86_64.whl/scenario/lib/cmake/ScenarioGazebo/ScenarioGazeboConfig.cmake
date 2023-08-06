set(ScenarioGazebo_VERSION 1.1.0)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was ScenarioGazeboConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

#### Expanded from @PACKAGE_DEPENDENCIES@ by install_basic_package_files() ####

include(CMakeFindDependencyMacro)
find_dependency(ScenarioCore)
find_dependency(ScenarioGazeboPlugins)
find_dependency(ignition-gazebo4)
find_dependency(ignition-common3)

###############################################################################


include("${CMAKE_CURRENT_LIST_DIR}/ScenarioGazeboTargets.cmake")




