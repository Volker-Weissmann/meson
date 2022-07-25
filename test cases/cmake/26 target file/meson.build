project('cmake_code_gen', ['c', 'cpp'])

# volker_inter_exe = executable('volker_inter_exe', 'volker_inter.cpp')

# gen_src = custom_target('gen-output',
#                         output : ['out.c'],
#                         command : [volker_inter_exe, '@OUTPUT@'], install: true, install_dir: '.')

# exe = executable('volker_exe', gen_src)

if meson.is_cross_build()
    message('Test skipped, see https://github.com/mesonbuild/meson/pull/10607#issuecomment-1188117276 for an explanation.')
else
    cm = import('cmake')

    # Subproject with the "code generator"
    sub_pro = cm.subproject('cmMod')
    sub_final = sub_pro.dependency('final', include_type: 'system')

    # Build the exe
    exe = executable('main', ['main.cpp'], dependencies: [sub_final])

    test('test', exe)

endif
