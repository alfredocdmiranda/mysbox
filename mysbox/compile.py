import os
import csv
import subprocess
from io import StringIO

build_dir = 'build_mys'

fqbn = {'uno': {'fqbn': 'arduino:avr:uno', 'label': 'Arduino/Genuino Uno'},
        'diecimila328': {'fqbn': 'arduino:avr:diecimila:cpu=atmega328', 'label': 'Arduino Diecimila or Duemilanove with Atmega328'},
        'diecimila168': {'fqbn': 'arduino:avr:diecimila:cpu=atmega168', 'label': 'Arduino Diecimila or Duemilanove with Atmega168'},
        'nano328': {'fqbn': 'arduino:avr:nano:cpu=atmega328', 'label': 'Arduino Nano with ATmega328'},
        'nano168': {'fqbn': 'arduino:avr:nano:cpu=atmega168', 'label': 'Arduino Nano with ATmega168'},
        'mega2560': {'fqbn': 'arduino:avr:mega:cpu=atmega2560', 'label': 'Arduino/Genuino Mega with ATmega2560'},
        'mega1280': {'fqbn': 'arduino:avr:mega:cpu=atmega1280', 'label': 'Arduino/Genuino Mega with ATmega1280'},
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
        print("".join(word.ljust(col_width) for word in [row, fqbn[row]['label']]))

    exit(0)


def _create_compiler_line(args, settings, build_path):
    board_str = fqbn[args.board]['fqbn']
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
