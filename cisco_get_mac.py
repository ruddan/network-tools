#!/usr/bin/python3

import argparse
from netmiko import ConnectHandler
from getpass import getpass


def main():
    parser = argparse.ArgumentParser(
        description="Find mac-address in mac-address table"
    )
    parser.add_argument(
        "filename",
        help="input filename, file should contain ip-address or hostname of the devices that the script should log into",
    )
    parser.add_argument("--mac", help="Locate mac-address", action="store_true")

    args = parser.parse_args()

    if not args.mac:
        print("missing --mac argument")
        return

    login(args)


def login(args):
    macaddr = input("\nmac-address: ").lower()
    username = input("Username: ")
    password = getpass()

    with open(args.filename) as devices:
        for line in devices:
            deviceaddr = line

            device = {
                "device_type": "cisco_ios",
                "host": deviceaddr,
                "username": username,
                "password": password,
                # 	'port' : 8022,          # optional, defaults to 22
            }

            net_connect = ConnectHandler(**device)
            hostname = net_connect.find_prompt()
            mac_table = net_connect.send_command(
                "sh mac address-table | inc " + macaddr
            )
            print(hostname)
            print(mac_table)


if __name__ == "__main__":
    main()
