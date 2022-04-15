import os
from datetime import datetime
from urllib.parse import unquote, urlsplit

import requests

from utils import download_image

COUNT_APOD_IMAGES = 20
API_EPIC_URL = 'https://api.nasa.gov/EPIC/api/natural/images?'
API_APOD_URL = 'https://api.nasa.gov/planetary/apod?'
EPIC_URL = 'https://api.nasa.gov/EPIC/archive/natural/'


def get_extension_from_url(url):
    url_split = urlsplit(url)
    return os.path.splitext(unquote(url_split.path))[1]


def fetch_nasa_epic(key):
    response = requests.get(f'{API_EPIC_URL}api_key={key}')
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        img_date = datetime.fromisoformat(img['date'])
        epic_photo_url = f'{EPIC_URL}{img_date.year}/' \
                         f'{img_date.month:02d}/' \
                         f'{img_date.day:02d}' \
                         f'/png/{img["image"]}.png?api_key={key}'
        download_image(epic_photo_url,
                       f'epic{img_number}.jpg')


def fetch_nasa_apod(key):
    response = requests.get(f'{API_APOD_URL}api_key={key}',
                            params={
                                'count': COUNT_APOD_IMAGES,
                                })
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        ext = get_extension_from_url(img['url'])
        if ext:
            download_image(img['url'], 
                           f'apod{img_number}{ext}')


def fetch_nasa(key):
    fetch_nasa_epic(key)
    fetch_nasa_apod(key)
