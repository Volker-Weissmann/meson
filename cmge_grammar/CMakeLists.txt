project (HELLO)

#cmake .. && grep echo CMakeFiles/genexdebug.dir/build.make

add_custom_target(genexdebug COMMAND ${CMAKE_COMMAND} -E echo "$><k<$<LOWER_CASE:ABC::,D>K:,>:$")
