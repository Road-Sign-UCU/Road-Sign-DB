import os
import random
import urllib3
import zipfile
import requests
from itertools import chain

def download_file(url, download_to, verify=True):
    print(f"Downloading {url.split('/')[-1]}...")
    if verify == False:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with requests.get(url, stream=True, verify=verify) as r:
        with open(download_to, 'wb') as f:
            # f.write(r.content)
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def unzip_file(zip_file, extract_to_dir):
    print(f"Unzipping {os.path.basename(zip_file)}...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)


def random_filename(length=8, extension="png"):
    choice_arr = [
        chr(char)
        for char in chain(
            range(ord('A'), ord('Z') + 1),
            range(ord('a'), ord('z') + 1),
            range(ord('0'), ord('9') + 1),
        )
    ]
    return ''.join(
        random.choice(choice_arr) for _ in range(length)
    ) + '.' + extension
