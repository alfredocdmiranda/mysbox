import os
import argparse

from mysbox import compile
from mysbox import create
from mysbox import config
from mysbox import upload


class ListBoardsCompileAction(argparse.Action):
    def __init__(self, option_strings=None, **kwargs):
        super(ListBoardsCompileAction, self).__init__(option_strings, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        compile.list_fqbn()


class ListBoardsUploadAction(argparse.Action):
    def __init__(self, option_strings=None, **kwargs):
        super(ListBoardsUploadAction, self).__init__(option_strings, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        upload.list_fqbn()


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    create_parser = subparsers.add_parser('create')
    create_subparser = create_parser.add_subparsers(dest='type_node', help="Type of sketch you want to create.")
    create_subparser.required = True

    create_node_parser = create_subparser.add_parser('node')
    create_node_parser.set_defaults(func=create.create_node)
    create_node_parser.add_argument('output', help="Output file name", nargs='?', default='node')
    create_node_parser.add_argument('-r', '--radio', help="Which type of radio will be enabled",
                                    default='NRF24', type=str.upper)
    create_node_parser.add_argument('-n', '--name', help="Sketch name", default='Sample', type=str)
    create_node_parser.add_argument('-v', '--version', help="Sketch version", default='1.0', type=str)
    create_node_parser.add_argument('-R', '--no-repeater', help="Disable repeater function", action='store_true')
    create_gw_parser = create_subparser.add_parser('gateway')
    create_gw_parser.set_defaults(func=create.create_gw)
    create_gw_parser.add_argument('output', help="Output file name", nargs='?', default='gw_node')
    create_gw_parser.add_argument('-t', '--type', help="Type of Gateway", default='serial', choices=['serial', 'eth'])
    create_gw_parser.add_argument('-r', '--radio', help="Wich type of radio will be enabled",
                                  default=None, type=str.upper)
    create_gw_parser.add_argument('-n', '--name', help="Sketch name", default=None, type=str)
    create_gw_parser.add_argument('-v', '--version', help="Sketch version", default=None, type=str)

    # connect_parser = subparsers.add_parser('connect')

    compile_parser = subparsers.add_parser('compile')
    compile_parser.set_defaults(func=compile.compile_mys)
    compile_parser.add_argument('sketch', help="Sketch file to be compiled")
    compile_parser.add_argument('-l', '--list', help="List all available boards", action=ListBoardsCompileAction, nargs=0)
    compile_parser.add_argument('-b', '--board', help="Target to be compiled", type=str.lower)

    upload_parser = subparsers.add_parser('upload')
    upload_parser.set_defaults(func=upload.upload_mys)
    upload_parser.add_argument('file', help="Hex file")
    upload_parser.add_argument('port', help="Serial port")
    upload_parser.add_argument('-l', '--list', help="List all available boards", action=ListBoardsUploadAction, nargs=0)
    upload_parser.add_argument('-b', '--board', help="Target to be compiled", type=str.lower)

    args = parser.parse_args()

    return args


def main():
    settings = config.load_config()
    args = arguments()
    args.func(args, settings)
