import json
import sys
from argparse import ArgumentParser

from datamx.models.values import GroupsSchema
from sunspec.core import client as client

from pysunspec_read.reader import Reader
from pysunspec_read.options import ConnectOptions

def run():
    parser = create_command_line_parser()
    args = parser.parse_args()
    data = Reader().read(ConnectOptions(device_type=args.device_type, ipaddr=args.ipaddr, slave_id=args.slave_id))
    # dump = json.dumps(data, sort_keys=True, indent=3, default=lambda x: x.__dict__)
    json_str = GroupsSchema().dumps(data, sort_keys=True, indent=3)
    print(json_str)

def create_command_line_parser():
    parser = ArgumentParser(usage='%(prog)s [options]')

    parser.add_argument('-c', '--device_type', metavar=' ',
                            default=client.TCP,
                            help='device type')
    parser.add_argument('-a', '--slave_id', metavar=' ', type=int,
                            default=1,
                            help='modbus slave address [default: 1]')
    parser.add_argument('-i', '--ipaddr', metavar=' ',
                            default='localhost',
                            help='ip address to use for modbus tcp [default: localhost]')
    parser.add_argument('-P', '--port', metavar=' ', type=int,
                            default=502,
                            help='port number for modbus tcp [default: 502]')
    parser.add_argument('-T', '--timeout', metavar=' ', type=float,
                            default=2.0,
                            help='timeout, in seconds (can be fractional, such as 1.5) [default: 2.0]')
    return parser


if __name__ == '__main__':
    # example command line args to pass to demo
    # --command="tcp" --ip_address="192.168.1.1"
    run()
