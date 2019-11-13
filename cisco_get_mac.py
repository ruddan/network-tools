#!/usr/bin/python3

import argparse
from netmiko import ConnectHandler
from getpass import getpass


def main():
    parser = argparse.ArgumentParser(
        description="Find mac-address in mac-address table"
    )
    parser.add_argument(
        "--i",
        dest="filename",
        help="input filename, file should contain ip-address or hostname of the devices that the script should log into",
    )
    parser.add_argument("--mac", help="which mac-address to search for", required=True)

    args = parser.parse_args()

    username = input("Username: ")
    password = getpass()

    with open(args.filename) as devices:
        for line in devices:
            deviceaddr = line

            mac(deviceaddr, username, password, args.mac)


def mac(deviceaddr, username, password, macaddr):

    device = {
        "device_type": "cisco_ios",
        "host": deviceaddr,
        "username": username,
        "password": password,
    }

    net_connect = ConnectHandler(**device)
    hostname = net_connect.find_prompt()
    mac_table = net_connect.send_command("sh mac address-table | inc " + macaddr)

    print(hostname)
    print(mac_table)


if __name__ == "__main__":
    main()
