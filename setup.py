import os
import json
import shutil
import requests

from tqdm import tqdm
from urllib import request
from urllib.request import urlopen, Request

server_dir = "fabric_server"
installer_jar = "installer.jar"
fabric_installer_api = "https://meta.fabricmc.net/v2/versions/installer"
minecraft_versions_api = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

print(f" ---------------------------------------------------------------------")
print(f"\tA simple script to download and install fabric server")
print(f" ---------------------------------------------------------------------")

def delete_fabric():
    if os.path.exists(server_dir):
        shutil.rmtree(server_dir)

def download_with_progress(url, destination):
    response = requests.get(url, stream = True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024   # 1 KB
    progress_bar = tqdm(
        total = total_size_in_bytes,
        unit = "B",
        unit_scale = True
    )

    with open(destination, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    
    progress_bar.close()

def download_minecraft_server_jar():
    http_req = Request(
        minecraft_versions_api,
        headers = {
            "Accept": "application/json"
        }
    )

    latest_ver = {}
    with urlopen(http_req) as res:
        res = json.loads(res.read().decode())
        latest_ver = res["latest"]
        
        for x in res["versions"]:
            print(f"v{x['id']} - {x['type']}")
        
        print(f"Latest release: {latest_ver['release']}")
        print(f"Latest snapshot: {latest_ver['snapshot']}")

        os.chdir(server_dir)
        os.system(f"java -jar {installer_jar} server -mcversion {latest_ver['release']} -downloadMinecraft")
        shutil.move("server.jar", "vanilla.jar")
        shutil.move("fabric-server-launch.jar", "server.jar")

        with open("fabric-server-launcher.properties", "a") as file:
            file.write("serverJar=vanilla.jar")
        with open("eula.txt", "w") as file:
            file.write("eula=true")
        
        sys_mem_mb = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**2)
        minecraft_mem = int(0.64 * sys_mem_mb)
        with open("start.sh", "w") as file:
            # file.write(f"screen -S minecraft_server java -Xmx{minecraft_mem}M -jar server.jar --nogui")
            file.write(f"java -Xmx2500M -jar server.jar --nogui")
        os.system("chmod +x start.sh")

def download_fabric():
    http_req = Request(
        fabric_installer_api,
        headers = {
            "Accept": "application/json"
        })

    with urlopen(http_req) as res:
        res = json.loads(res.read().decode())
        fabric_dict = {}

        for x in res:
            fabric_dict[x["version"]] = {
                "stable": x["stable"],
                "url": x["url"]
            }
            version = x["version"]
            stable = "stable" if x["stable"] else "not_stable"
            print(f"{version} - {stable}")
            
        user_version = input(f"Which version? ").strip()
        print(f"Downloading Fabric v{user_version} ...")
        download_with_progress(fabric_dict[user_version]["url"], installer_jar)
        shutil.move(installer_jar, server_dir)
        
        download_minecraft_server_jar()

if not os.path.exists(server_dir):
    os.mkdir(server_dir)
    download_fabric()
else:
    if len(os.listdir(server_dir)) != 0:
        ans = input(f"{server_dir} directory is not empty. Proceed to replace it with fresh server installation? (y/N) ").strip().lower()

        if ans == "y":
            print(f"Proceed")
            download_fabric()
        else:
            print(f"Keep existing server")
    else:
        download_fabric()