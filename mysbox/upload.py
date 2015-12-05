import os
import csv
import subprocess
from io import StringIO

fqbn = {'uno': ['atmega328p', '115200', 'Arduino Uno'],
        'duemilanove': ['atmega328p', '115200', 'Arduino Diecimila or Duemilanove with Atmega328']
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
        print("".join(word.ljust(col_width) for word in [row, fqbn[row][-1]]))

    exit(0)


def _upload_line(args, settings):
    avrdude = os.path.join(settings['compiler']['arduino_tools'], 'avrdude')
    avrdude_conf = os.path.join(settings['compiler']['arduino_tools'], 'etc/avrdude.conf')
    baudrate = fqbn[args.board][1]
    micro = fqbn[args.board][0]
    port = args.port
    hexfile = args.file

    upload_line = "{0} -C{1} -v -p{2} -carduino -P{3} -b{4} -D -Uflash:w:{5}:i".format(avrdude, avrdude_conf, micro,
                                                                                       baudrate, port, hexfile)

    return upload_line
