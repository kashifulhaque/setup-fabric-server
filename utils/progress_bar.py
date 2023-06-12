import requests
from tqdm import tqdm

destination = "installer.jar"

def download_with_progress(url):
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
    return destination