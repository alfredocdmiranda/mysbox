import cmd
import threading
from queue import Empty

from pymys import mysensors as mys

from mysbox.utils import IndexableQueue

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
        try:
            for i in range(msg_queue.qsize()):
                print(msg_queue[i])
        except Empty:
            print("No message to show.")

    def do_list(self, line):
        print(line)
        for n in self.gw.nodes:
            print(self.gw.nodes[n])

    def do_exit(self, line):
        print("Exiting...")
        self.exiting[0] = True
        self.thread.join()
        exit(0)