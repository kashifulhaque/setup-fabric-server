import os
import json
import shutil
from colorama import Fore, Style
from urllib.request import urlopen, Request
from utils.progress_bar import download_with_progress

# Set colorama to work with ANSI escape sequences on Windows
if os.name == 'nt':
    import colorama
    colorama.init()

def download_fabric(download_url, server_dir):
    try:
        http_req = Request(download_url, headers = {"Accept": "application/json"})
        with urlopen(http_req) as res:
            data = json.loads(res.read().decode())
    except ConnectionError as e:
        print(Fore.RED + f"An error occurred while downloading Fabric loader: {e}" + Style.RESET_ALL)
        return None

    try:
        stable_version = data[0]
        url = stable_version["url"]
        version = stable_version["version"]

        print(Fore.GREEN + f"Downloading Fabric v{version} ..." + Style.RESET_ALL)
        installer_jar = download_with_progress(url)
        shutil.move(installer_jar, server_dir)
        return installer_jar
    except (IndexError, KeyError) as e:
        print(Fore.RED + f"An error occurred while processing Fabric data: {e}" + Style.RESET_ALL)
        return None