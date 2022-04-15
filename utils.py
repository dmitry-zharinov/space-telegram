from pathlib import Path

import requests


IMG_FOLDER_NAME = 'images'


def download_image(url, filename, payload):
    response = requests.get(url, payload)
    response.raise_for_status()
    with open(Path(IMG_FOLDER_NAME) / filename, 'wb') as file:
        file.write(response.content)