import os
import csv
import subprocess
from io import StringIO

fqbn = {'uno': {'cpu': 'atmega328p', 'protocol': 'arduino', 'baudrate': '115200',
                'label': 'Arduino/Genuino Uno'},
        'diecimila328': {'cpu': 'atmega328p', 'protocol': 'arduino', 'baudrate': '57600',
                         'label': 'Arduino Duemilanove or Diecimila with ATmega328'},
        'diecimila168': {'cpu': 'atmega168', 'protocol': 'arduino', 'baudrate': '19200',
                         'label': 'Arduino Duemilanove or Diecimila with ATmega168'},
        'nano328': {'cpu': 'atmega328p', 'protocol': 'arduino', 'baudrate': '57600',
                    'label': 'Arduino Nano with ATmega328'},
        'nano168': {'cpu': 'atmega168', 'protocol': 'arduino', 'baudrate': '19200',
                    'label': 'Arduino Nano with ATmega168'},
        'mega2560': {'cpu': 'atmega2560', 'protocol': 'wiring', 'baudrate': '115200',
                     'label': 'Arduino/Genuino Mega with ATmega2560'},
        'mega1280': {'cpu': 'atmega1280', 'protocol': 'arduino', 'baudrate': '57600',
                     'label': 'Arduino/Genuino Mega with ATmega1280'},
        }


def upload_mys(args, settings):
    upload_line = _upload_line(args, settings)

    code = subprocess.call([j for i in csv.reader(StringIO(upload_line), delimiter=' ') for j in i])

    return code


def list_fqbn():
    col_width = max(len(row) for row in fqbn) + 10

    print("List of available boards:\n")
    print("".join(word.ljust(col_width) for word in ['Argument', 'Name']))
    for row in sorted(fqbn):
        print("".join(word.ljust(col_width) for word in [row, fqbn[row]['label']]))

    exit(0)


def _upload_line(args, settings):
    avrdude = os.path.join(settings['compiler']['arduino_tools'], 'bin/avrdude')
    avrdude_conf = os.path.join(settings['compiler']['arduino_tools'], 'etc/avrdude.conf')
    port = args.port
    hexfile = args.file

    upload_line = "{0} -C{1} -v -p{fqbn[cpu]} -c{fqbn[protocol]} -P{2} -b{fqbn[baudrate]} -D -Uflash:w:{3}:i".format(
                                                                                    avrdude, avrdude_conf, port,
                                                                                    hexfile, fqbn=fqbn[args.board])

    return upload_line
