import os
import csv
import subprocess
from io import StringIO

build_dir = 'build_mys'

fqbn = {'uno': ['arduino:avr:uno', 'Arduino Uno'],
        'duemilanove': ['arduino:avr:diecimila:cpu=atmega328', 'Arduino Diecimila or Duemilanove with Atmega328']
        }


def compile_mys(args, settings):
    path, filename = os.path.split(os.path.abspath(args.sketch))
    build_path = _check_build_path(path)

    compiler_line = _create_compiler_line(args, settings, build_path)

    code = subprocess.call([j for i in csv.reader(StringIO(compiler_line), delimiter=' ') for j in i])

    return code


def list_fqbn():
    col_width = max(len(row) for row in fqbn) + 10

    print("List of available boards:\n")
    print("".join(word.ljust(col_width) for word in ['Argument', 'Name']))
    for row in sorted(fqbn):
        print("".join(word.ljust(col_width) for word in [row, fqbn[row][1]]))

    exit(0)


def _create_compiler_line(args, settings, build_path):
    board_str = fqbn[args.board][0]
    libs = csv.reader(StringIO(settings['compiler']['libs']), delimiter=',')

    libs_str = ''
    for row in libs:
        for l in row:
            libs_str += '-libraries "{}" '.format(l)

    compiler_line = '{s[arduino_builder]} -compile -logger=machine -hardware "{s[arduino_hardware]}" ' \
                    '-tools "{s[builder_tools]}" -tools "{s[arduino_tools]}" -built-in-libraries {s[builtin_libs]} ' \
                    '{0}-fqbn={1} -ide-version={s[ide_version]} -build-path "{2}" -warnings=none ' \
                    '-prefs=build.warn_data_percentage=75 -verbose "{3}"'.format(libs_str, board_str,
                                                                                 build_path, args.sketch,
                                                                                 s=settings['compiler'])

    return compiler_line


def _check_build_path(path):
    build_path = os.path.join(path, build_dir)
    if not os.path.exists(build_path):
        os.mkdir(build_path)

    return build_path
