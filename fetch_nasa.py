import os
from datetime import datetime
from urllib.parse import unquote, urlsplit

import requests

from utils import download_image

COUNT_APOD_IMAGES = 20


def get_extension_from_url(url):
    url_split = urlsplit(url)
    return os.path.splitext(unquote(url_split.path))[1]


def fetch_nasa_epic(key):
    api_img_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    api_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    payload = {
        'api_key': key,
        'count': COUNT_APOD_IMAGES,
    }
    response = requests.get(api_img_url, params=payload)
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        img_date = datetime.fromisoformat(img['date'])
        year = img_date.year
        month = img_date.month
        day = img_date.day
        filename = f'{img["image"]}.png'
        img_url = f'{api_url}{year}/{month:02d}/{day:02d}/png/{filename}'
        img_payload = {
            'api_key': key,
        }
        download_image(img_url,
                       f'epic{img_number}.jpg',
                       img_payload)


def fetch_nasa_apod(key):
    api_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    payload = {
        'api_key': key,
        'count': COUNT_APOD_IMAGES,
    }
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        ext = get_extension_from_url(img['url'])
        if ext:
            download_image(img['url'],
                           f'apod{img_number}{ext}',
                           None)


def fetch_nasa(key):
    fetch_nasa_epic(key)
    fetch_nasa_apod(key)
