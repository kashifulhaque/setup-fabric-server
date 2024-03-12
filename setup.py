import os
from colorama import Fore, Style
from utils.prompts import prompt_confirmation
from utils.download_fabric_loader import download_fabric
from utils.download_minecraft_server import download_server_jar

server_dir = "fabric_server"
fabric_installer_url = "https://meta.fabricmc.net/v2/versions/installer"
minecraft_versions_api = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def main():
    print(Fore.CYAN + " --------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.CYAN + "          A simple script to download the latest Minecraft fabric server         " + Style.RESET_ALL)
    print(Fore.CYAN + " --------------------------------------------------------------------------------" + Style.RESET_ALL)

    if os.path.exists(server_dir):
        print(Fore.YELLOW + f"{server_dir} directory already exists\nExiting ..." + Style.RESET_ALL)
        return

    os.makedirs(server_dir, exist_ok=True)

    installer_jar = download_fabric(fabric_installer_url, server_dir)
    if installer_jar is None:
        print(Fore.RED + "Failed to download Fabric installer. Exiting..." + Style.RESET_ALL)
        return

    download_server_jar(minecraft_versions_api, server_dir, installer_jar)

if __name__ == "__main__":
    main()
