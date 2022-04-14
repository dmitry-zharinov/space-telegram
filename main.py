import logging
import os
import time
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv

from fetch_nasa import fetch_nasa_APOD, fetch_nasa_EPIC
from fetch_spacex import fetch_spacex

IMG_FOLDER_NAME = 'images'


def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path(IMG_FOLDER_NAME) / filename, 'wb') as file:
        file.write(response.content)


def publish_photo(path):
    bot = telegram.Bot(token=os.environ['TG_BOT_TOKEN'])
    bot.send_document(chat_id=os.environ['TG_CHAT_ID'],
                      document=open(path, 'rb'))


def main():
    load_dotenv()
    logging.basicConfig(handlers=[logging.FileHandler(filename="./app.log",
                                                      encoding='utf-8',
                                                      mode='a+')],
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%F %A %T')
    Path(IMG_FOLDER_NAME).mkdir(parents=True, exist_ok=True)

    fetch_spacex()
    fetch_nasa_EPIC()
    fetch_nasa_APOD()

    for i in os.walk(IMG_FOLDER_NAME):
        for img in i[2]:
            time.sleep(int(os.environ['PHOTO_PUBLISH_PERIOD']))
            publish_photo(os.fspath(Path(IMG_FOLDER_NAME) / img))
            logging.info(f'Опубликовано фото {img}')


if __name__ == '__main__':
    main()
