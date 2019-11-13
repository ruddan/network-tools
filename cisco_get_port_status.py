#!/usr/bin/python3

import argparse
from netmiko import ConnectHandler
from getpass import getpass
import re
from pprint import pprint


def main():

    parser = argparse.ArgumentParser(
        description="Locate ports based on connection status"
    )
    parser.add_argument(
        "--i",
        dest="filename",
        required=True,
        help="input filename, file should contain ip-address or hostname of the devices that the script should log into",
    )
    parser.add_argument(
        "--status",
        choices=("connected", "notconnect", "err-disable"),
        help="connected, notconnect or err-disable",
    )

    args = parser.parse_args()
    username = input("Username: ")
    password = getpass()

    with open(args.filename) as devices:
        # Fetch devices from input file
        for line in devices:
            deviceaddr = line

            if args.status:
                sh_int_status = run_command(
                    args, deviceaddr, username, password, "show int status"
                )
                parsed = parse_ports(sh_int_status)
                get_port_status(parsed, args.status)


def run_command(args, deviceaddr, username, password, command):

    device = {
        "device_type": "cisco_ios",
        "host": deviceaddr,
        "username": username,
        "password": password,
    }

    net_connect = ConnectHandler(**device)
    hostname = net_connect.find_prompt()
    print(hostname)
    cmd = net_connect.send_command(command)
    return cmd


def parse_ports(cmd_output):

    # Split output at newline
    # Interfaces start at index [2]
    s_status_split = cmd_output.split("\n")
    port_rows = s_status_split[2:]

    list_ports = {}
    for p in port_rows:
        # Loop is executed on all rows in port_rows
        # Split line on whitespaces
        # 1. Fetch array index for interface names and split on whitespaces
        # 2. Fetch array starting index for port status and split on whitespaces
        # 3. Create a dict with port_name as key
        port_name = p.split()[0]
        port_status = p[29:].split()

        list_ports[port_name] = {
            "status": port_status[0],
            "vlan": port_status[1],
            "duplex": port_status[2],
            "speed": port_status[3],
            "type": port_status[4],
        }
    return list_ports


def get_port_status(parsed, status):

    port_list = {k: v for k, v in parsed.items() if v["status"] == status}
    for key, value in port_list.items():
        print("{}: {}".format(key, value["status"]))
    print("Ports: {}".format(len(port_list)))


if __name__ == "__main__":
    main()
