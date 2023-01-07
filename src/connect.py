import os

os.system('notify-send "Connecting to VPN..."')
from get_password import get_password_for_region
import requests

FILENAME = "pass.txt"
USERNAME = "freeopenvpn"
CONFIG_URL_PATTERN = "https://www.freeopenvpn.org/ovpn/{}_freeopenvpn_{}.ovpn"


def write_config_to_file(region, connect_type, file_path):
    config_url = CONFIG_URL_PATTERN.format(region, connect_type.lower())
    with open(file_path, "w") as f:
        content = requests.get(config_url).content.decode()
        f.write(content)
    return file_path


def connect(region, connect_type):
    config_name = f"{region}_freeopenvpn_{connect_type}"
    config_path = f"/tmp/{config_name}.ovpn"
    password = get_password_for_region(region, n=3)

    write_config_to_file(region, connect_type, config_path)
    os.system(f"nmcli c delete {config_name}")
    os.system(f"nmcli c import type openvpn file {config_path}")
    os.system(f"nmcli c modify {config_name} vpn.secrets 'username={USERNAME}'")
    os.system(f"nmcli c modify {config_name} vpn.secrets 'password={password}'")
    os.system(f"nmcli c up {config_name}")


if __name__ == "__main__":
    # USA, UK, Russia-2, Russia-3, Germany, Netherlands
    # region = "USA"
    region = "UK"
    # region = "Russia-2"
    # region = "Netherlands"
    # region = "Germany"
    # UDP, TCP
    connect_type = "UDP"
    connect(region, connect_type)
