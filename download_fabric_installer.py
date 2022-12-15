import os
from urllib import request
from urllib.request import urlopen, Request
import json

if not os.path.exists('fabric_server'):
  api_url = 'https://meta.fabricmc.net/v2/versions/installer'
  download_url = ''

  http_request = Request(api_url, headers = {
    "Accept": "application/json"
  })

  with urlopen(http_request) as res:
    res = json.loads(res.read().decode())
    
    for x in res:
      if x['stable']:
        download_url = x['url']
        break

  request.urlretrieve(download_url, 'installer.jar')
  os.mkdir('fabric_server')
  os.system('mv installer.jar fabric_server')
