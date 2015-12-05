import os
import csv

build_dir = 'build_mys'

fqbn = {'uno': ['arduino:avr:uno', 'Arduino Uno'],
        'duemilanove': ['arduino:avr:diecimila:cpu=atmega328', 'Arduino Diecimila or Duemilanove with Atmega328']
        }


def compile_mys(args, settings):
    path, filename = os.path.split(os.path.abspath(args.sketch))
    build_path = _check_build_path(path)

    compiler_line = _create_compiler_line(args, settings, build_path)

    print(compiler_line)


def list_fqbn():
    col_width = max(len(row) for row in fqbn) + 10  # padding

    print("List of available boards:\n")
    print("".join(word.ljust(col_width) for word in ['Argument', 'Name']))
    for row in sorted(fqbn):
        print("".join(word.ljust(col_width) for word in [row, fqbn[row][1]]))

    exit(0)


def _create_compiler_line(args, settings, build_path):
    # arduino_builder = settings['compiler'].get('arduino_builder')
    # arduino_hardware = settings['compiler'].get('arduino_hardware')
    # arduino_tools = settings['compiler'].get('arduino_tools')
    # builder_tools = settings['compiler'].get('builder_tools')
    # ide_version = settings['compiler'].get('ide_version')
    # builtin_libs = settings['compiler'].get('builtin_libs')
    libs = settings['compiler'].get('libs').split(",")
    print(libs)
    libs_str = ''
    for l in libs:
        libs_str += '-libraries "{}" '.format(l)

    compiler_line = '{s[arduino_builder]} -compile -logger=machine -hardware "{s[arduino_hardware]}" ' \
                    '-tools "{s[builder_tools]}" -tools "{s[arduino_tools]}" -built-in-libraries {s[builtin_libs]} ' \
                    '{0}-fqbn={1} -ide-version={s[ide_version]} -build-path "{2}" -warnings=none ' \
                    '-prefs=build.warn_data_percentage=75 -verbose "{3}"'.format(libs_str, fqbn[args.board][0],
                                                                                 build_path, args.sketch,
                                                                                 s=settings['compiler'])

    return compiler_line


def _check_build_path(path):
    build_path = os.path.join(path, build_dir)
    if not os.path.exists(build_path):
        os.mkdir(build_path)

    return build_path
