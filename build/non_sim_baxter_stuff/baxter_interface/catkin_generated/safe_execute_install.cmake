execute_process(COMMAND "/home/evana/apv_ws/build/non_sim_baxter_stuff/baxter_interface/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/evana/apv_ws/build/non_sim_baxter_stuff/baxter_interface/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
