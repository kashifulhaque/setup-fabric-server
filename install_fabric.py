import os
import sys

if len(sys.argv) != 2:
  print('Argument missing: Minecraft version')
else:
  version = sys.argv[1]

  if os.path.exists('fabric_server/installer.jar'):
    os.chdir('fabric_server')
    os.system(f'java -jar installer.jar server -mcversion {version} -downloadMinecraft')
    os.system('mv server.jar vanilla.jar')
    os.system('mv fabric-server-launch.jar server.jar')
    os.system('echo "serverJar=vanilla.jar" > fabric-server-launcher.properties')
    os.system('echo "eula=true" > eula.txt')

    sys_mem_mb = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**2)
    minecraft_mem = int(0.75 * sys_mem_mb)

    with open('start.sh', 'w') as file:
      file.write(f'screen -S minecraft_server java -Xmx{minecraft_mem}M -jar server.jar --nogui')
    
    os.system('chmod +x start.sh')
  else:
    print('fabric_server/installer.jar missing, run download_fabric_installer.py first')
