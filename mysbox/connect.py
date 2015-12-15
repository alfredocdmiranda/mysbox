import cmd
import threading
from queue import Empty

from pymys import mysensors as mys

from mysbox.utils import IndexableQueue
from mysbox.utils import ThrowingArgumentParser, ArgumentParserError

msg_queue = IndexableQueue()


def connect_gw(args, settings):
    term = MysTerminal(args.port)
    term.prompt = "[mysbox] > "
    term.cmdloop()


def queue_msg(msg):
    if msg_queue.full():
        msg_queue.get()
    msg_queue.put(msg)


def run_gateway(gw, stop):
    while not stop[0]:
        gw.process()
    gw.disconnect()


class MysTerminal(cmd.Cmd):
    def __init__(self, port, *args, **kwargs):
        self.port = port
        self.gw = mys.SerialGateway(self.port, message_callback=queue_msg)
        self.exiting = [False]

        try:
            self.gw.connect()
        except mys.GatewayError as err:
            print("Not possible to connect to Gateway: {}".format(err))
            exit(1)
        self.thread = threading.Thread(target=run_gateway, args=[self.gw, self.exiting])
        self.thread.start()
        super(MysTerminal, self).__init__(*args, **kwargs)

    def do_show(self, line):
        line = [i for i in line.split(" ") if i]
        parser = ThrowingArgumentParser(prog="show", add_help=False)
        parser.add_argument("-h", "--help", action='store_true')

        try:
            args = parser.parse_args(line)
        except ArgumentParserError as err:
            print(err)
        else:
            try:
                for i in range(msg_queue.qsize()):
                    print(msg_queue[i])
            except Empty:
                print("No message to show.")

    def do_send(self, line):
        line = [i for i in line.split(" ") if i]
        parser = ThrowingArgumentParser(prog="send", add_help=False)
        parser.add_argument("message", nargs='?')
        parser.add_argument("-h", "--help", action='store_true')

        try:
            args = parser.parse_args(line)
        except ArgumentParserError as err:
            print(err)
        else:
            try:
                msg = mys.Message(args.message)
                self.gw.send(msg)
            except mys.BadMessageError as err:
                print(err)

    def do_list(self, line):
        line = [i for i in line.split(" ") if i]
        parser = ThrowingArgumentParser(prog="list", add_help=False)
        parser.add_argument("device", choices=['nodes', 'sensors'], nargs='?')
        parser.add_argument("-h", "--help", action='store_true')

        try:
            args = parser.parse_args(line)
        except ArgumentParserError as err:
            print(err)
        else:
            if args.help:
                parser.print_help()
                return
            if args.device == 'nodes':
                if not self.gw.nodes:
                    print("There is no Node attached to this Gateway.")
                else:
                    for n in self.gw.nodes:
                        print(self.gw[n])
            elif args.device == 'sensors':
                try:
                    if not self.gw[line[1]].sensors:
                        print("There is no Sensor attached to this Node.")
                    else:
                        for s in self.gw[line[1]].sensors:
                            print(self.gw[line[1]][s])
                except KeyError as err:
                    print("There is no Node with this ID {}".format(err))
            else:
                parser.print_usage()

    def do_reboot(self, line):
        line = [i for i in line.split(" ") if i]
        parser = ThrowingArgumentParser(prog="reboot", add_help=False)
        parser.add_argument("node_id", nargs='?')
        parser.add_argument("-h", "--help", action='store_true')

        try:
            args = parser.parse_args(line)
        except ArgumentParserError as err:
            print(err)
        else:
            if args.help:
                parser.print_help()
                return
            if args.node_id == 'all':
                for n in self.gw.nodes:
                    self.gw.reboot(n)
            elif args.node_id.isdigit():
                if int(args.node_id) in self.gw.nodes:
                    self.gw.reboot(int(args.node_id))
                else:
                    print("There is no Node with this ID {}".format(args.node_id))
            else:
                parser.print_usage()

    def do_EOF(self, line):
        self.do_exit(line)

    def do_exit(self, line):
        print("Exiting...")
        self.exiting[0] = True
        self.thread.join()
        exit(0)