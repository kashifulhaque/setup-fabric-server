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

def download_fabric(download_url: str, server_dir: str) -> str:
    """
    Download the Fabric loader from the given URL and save it to the specified directory.

    Parameters:
    - download_url (str): The URL to download the Fabric loader JSON data from.
    - server_dir (str): The directory where the downloaded Fabric loader JAR file will be saved.

    Returns:
    - str: The path to the downloaded Fabric loader JAR file, or None if an error occurs.
    """
    try:
        http_req = Request(download_url, headers={"Accept": "application/json"})
        with urlopen(http_req) as res:
            data = json.loads(res.read().decode())
    except ConnectionError as e:
        print(Fore.RED + f"An error occurred while downloading Fabric loader: {e}" + Style.RESET_ALL)
        return None

    try:
        stable_version = data[0]
        url = stable_version.get("url")
        version = stable_version.get("version")

        if not url or not version:
            raise KeyError("Missing required fields in Fabric data")

        print(Fore.GREEN + f"Downloading Fabric v{version} ..." + Style.RESET_ALL)
        installer_jar = download_with_progress(url)
        shutil.move(installer_jar, server_dir)
        return installer_jar
    except (IndexError, KeyError) as e:
        print(Fore.RED + f"An error occurred while processing Fabric data: {e}" + Style.RESET_ALL)
        return None
