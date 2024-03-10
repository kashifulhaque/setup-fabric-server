import os
import json
import shutil
import subprocess
from colorama import Fore, Style
from urllib.request import urlopen, Request

if os.name == 'nt':
    import colorama
    colorama.init()

multiplier = 0.7

def get_latest_release(url):
    try:
        http_req = Request(url, headers={"Accept": "application/json"})
        with urlopen(http_req) as data:
            data = json.loads(data.read().decode())
    except ConnectionError as e:
        print(Fore.RED + f"An error occurred while downloading Minecraft server: {e}" + Style.RESET_ALL)
        return None
    
    return data["latest"]["release"]

def download_server_jar(url, server_dir, installer_jar):
    latest_release = get_latest_release(url)
    print(Fore.GREEN + f"Downloading Minecraft v{latest_release}" + Style.RESET_ALL)

    os.chdir(server_dir)
    server_command = f"java -jar {installer_jar} server -mcversion {latest_release} -downloadMinecraft"
    try:
        result = subprocess.check_output(server_command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"An error occurred while executing server command: {e.output.decode()}" + Style.RESET_ALL)
        return

    output_lines = result.decode().splitlines()
    for line in output_lines[:-1]:
        print(line)
    
    shutil.move("server.jar", "vanilla.jar")
    shutil.move("fabric-server-launch.jar", "server.jar")
    with open("fabric-server-launcher.properties", "a") as file:
        file.write("serverJar=vanilla.jar")
    with open("eula.txt", "w") as file:
        file.write("eula=true")
    
    # Retrieve system memory size in megabytes
    page_size = os.sysconf('SC_PAGE_SIZE')  # System page size in bytes
    phys_pages = os.sysconf('SC_PHYS_PAGES')  # Total number of physical pages
    sys_mem_mb = (page_size * phys_pages) / (1024.0 ** 2)  # System memory size in megabytes

    # Calculate Minecraft server memory based on a multiplier
    minecraft_mem = int(multiplier * sys_mem_mb)    # Minecraft server memory in megabytes
    
    # Write the server start command to a shell script file
    with open("start.sh", "w") as file:
        file.write(f"screen -S minecraft_server java -Xmx{minecraft_mem}M -jar server.jar --nogui")
    
    os.system("chmod +x start.sh")
    print(Fore.GREEN + f"To start the server, run: {os.path.join(server_dir, 'start.sh')}" + Style.RESET_ALL)
