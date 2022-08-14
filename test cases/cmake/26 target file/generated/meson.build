project('cmMod', 'cpp', 'c')
cm_exe_local_dir = include_directories('__CMake_build', '.')
cm_exe_local_sys = include_directories(is_system : true)
cm_exe_local_inc = [cm_exe_local_dir, cm_exe_local_sys]
cm_exe_local_src = files('local.cpp')
cm_exe_local = executable(
  'cm_exe_local',
  cm_exe_local_src,
  build_by_default : false,
  link_args : [],
  link_with : [],
  include_directories : cm_exe_local_inc,
  install : false,
  override_options : ['cpp_std=gnu++14'],
  objects : [],
  cpp_args : [],
  pie : false
)
custom_tgt_0 = custom_target(
  'custom_tgt_0',
  input : ['input1.txt'],
  output : ['output1.cpp'],
  command : [
    '/usr/bin/meson',
    '--internal',
    'cmake_run_ctgt',
    '-o',
    '@OUTPUT@',
    '-O',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build/output1.cpp',
    '-d',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/subprojects/cmMod/input1.txt',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build/output1.cpp',
    ';;;'
  ],
  depends : [cm_exe_local]
)
custom_tgt_1 = custom_target(
  'custom_tgt_1',
  input : ['input2.txt'],
  output : ['output2.cpp'],
  command : [
    '/usr/bin/meson',
    '--internal',
    'cmake_run_ctgt',
    '-o',
    '@OUTPUT@',
    '-O',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build/output2.cpp',
    '-d',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build',
    '/usr/bin/cp',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/subprojects/cmMod/input2.txt',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build/output2.cpp',
    ';;;'
  ],
  depends : []
)
output1_cpp = custom_target(
  'output1_cpp',
  input : [custom_tgt_0],
  output : ['output1_cpp.h'],
  command : [
    '/usr/bin/meson',
    '--internal',
    'cmake_run_ctgt',
    '-o',
    '@OUTPUT@',
    '-d',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build'
  ],
  depends : []
)
output2_cpp = custom_target(
  'output2_cpp',
  input : [custom_tgt_1],
  output : ['output2_cpp.h'],
  command : [
    '/usr/bin/meson',
    '--internal',
    'cmake_run_ctgt',
    '-o',
    '@OUTPUT@',
    '-d',
    '/home/volker/Sync/git/meson/test cases/cmake/26 target file/build/subprojects/cmMod/__CMake_build'
  ],
  depends : []
)
final_dir = include_directories('include', '__CMake_build', '.')
final_sys = include_directories(is_system : true)
final_inc = [final_dir, final_sys]
final_src = files('final.cpp')
final = shared_library(
  'final',
  final_src,
  custom_tgt_0,
  custom_tgt_1,
  output1_cpp,
  output2_cpp,
  build_by_default : false,
  link_args : [],
  link_with : [],
  include_directories : final_inc,
  install : false,
  override_options : ['cpp_std=gnu++14'],
  objects : [],
  cpp_args : ['-Dfinal_EXPORTS'],
  c_args : []
)
final_dep = declare_dependency(
  link_args : [],
  link_with : final,
  compile_args : [],
  include_directories : final_inc
)
