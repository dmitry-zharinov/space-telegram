import os
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit
import logging

import requests
from dotenv import load_dotenv
import telegram

IMG_FOLDER_NAME = 'images'
COUNT_APOD_IMAGES = 20
TG_CHAT_ID = '@dw_space_photos'


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_extension_from_url(url):
    url_split = urlsplit(url)
    return os.path.splitext(unquote(url_split.path))[1]


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v5/launches/')
    response.raise_for_status()
    images = response.json()[12]['links']['flickr']['original']
    for img_number, img_url in enumerate(images):
        download_image(img_url,
                       Path(IMG_FOLDER_NAME) / (f'spacex{img_number}.jpg'))


def fetch_nasa_epic_photo():
    response = requests.get(f'https://api.nasa.gov/EPIC/api/natural/images?'
                            f'api_key={os.environ["NASA_API_KEY"]}')
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        img_date = datetime.fromisoformat(img['date'])
        epic_photo_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
                         f'{img_date.year}/' \
                         f'{img_date.month:02d}/' \
                         f'{img_date.day:02d}' \
                         f'/png/{img["image"]}.png?api_key=DEMO_KEY'
        download_image(epic_photo_url,
                       Path(IMG_FOLDER_NAME) / (f'epic{img_number}.jpg'))


def fetch_nasa_APOD():
    payload = {
        'count': COUNT_APOD_IMAGES,
    }
    response = requests.get(f'https://api.nasa.gov/planetary/apod?'
                            f'api_key={os.environ["NASA_API_KEY"]}',
                            params=payload)
    response.raise_for_status()
    for img_number, img in enumerate(response.json()):
        ext = get_extension_from_url(img['url'])
        download_image(img['url'],
                       Path(IMG_FOLDER_NAME)
                       / (f'apod{img_number}{ext}'))


def publish_photo(path):
    bot = telegram.Bot(token=os.environ['TG_BOT_TOKEN'])
    bot.send_document(chat_id=TG_CHAT_ID,
                      document=open(path, 'rb'))


def main():
    load_dotenv()
    Path(IMG_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
    # fetch_spacex_last_launch()
    # fetch_nasa_epic_photo()
    # fetch_nasa_APOD()
    for i in os.walk(os.fspath(Path(IMG_FOLDER_NAME))):
        for img in i[2]:
            # print(Path(IMG_FOLDER_NAME) / img)
            time.sleep(int(os.environ['PHOTO_PUBLISH_PERIOD']))
            publish_photo(os.fspath(Path(IMG_FOLDER_NAME) / img))
            logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                                filename='app.log',
                                filemode='w')
            logging.info(f'Опубликовано фото {img}')


if __name__ == '__main__':
    main()
