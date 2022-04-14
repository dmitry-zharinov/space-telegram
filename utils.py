from pathlib import Path

import requests


IMG_FOLDER_NAME = 'images'


def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(IMG_FOLDER_NAME) / filename, 'wb') as file:
        file.write(response.content)