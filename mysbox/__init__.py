import os
import argparse

from mysbox import create
from mysbox import config


def arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    create_parser = subparsers.add_parser('create')
    create_subparser = create_parser.add_subparsers(dest='type', help="Type of sketch you want to create.")
    create_subparser.required = True

    create_node_parser = create_subparser.add_parser('node')
    create_node_parser.set_defaults(func=create.create_node)
    create_node_parser.add_argument('output', help="Output file name", nargs='?', default='node.ino')
    create_node_parser.add_argument('-r', '--radio', help="Which type of radio will be enabled",
                                    default='NRF24', type=str.upper)
    create_node_parser.add_argument('-n', '--name', help="Sketch name", default='Sample', type=str)
    create_node_parser.add_argument('-v', '--version', help="Sketch version", default='1.0', type=str)
    create_node_parser.add_argument('-R', '--no-repeater', help="Disable repeater function", action='store_true')
    create_gw_parser = create_subparser.add_parser('gateway')
    create_gw_parser.set_defaults(func=create.create_gw)
    create_gw_parser.add_argument('output', help="Output file name", nargs='?', default='gw_node.ino')
    create_gw_parser.add_argument('-t', '--type', help="Type of Gateway", default='serial', choices=['serial', 'eth'])
    create_gw_parser.add_argument('-r', '--radio', help="Wich type of radio will be enabled",
                                  default=None, type=str.upper)
    create_gw_parser.add_argument('-n', '--name', help="Sketch name", default=None, type=str)
    create_gw_parser.add_argument('-v', '--version', help="Sketch version", default=None, type=str)

    connect_parser = subparsers.add_parser('connect')

    args = parser.parse_args()

    return args


def main():
    settings = config.load_config()
    # print(type(settings['default']['arduino_path']))
    args = arguments()
    args.func(args)