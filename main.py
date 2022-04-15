import logging
import os
import time
from pathlib import Path

import telegram
from dotenv import load_dotenv

from fetch_nasa import fetch_nasa
from fetch_spacex import fetch_spacex

IMG_FOLDER_NAME = 'images'


def publish_photo(path, token, chat_id):
    bot = telegram.Bot(token=token)
    with open(path, 'rb') as photo:
        bot.send_document(chat_id=chat_id,
                          document=photo)


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
    fetch_nasa(os.environ["NASA_API_KEY"])

    telegram_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    for i in os.walk(IMG_FOLDER_NAME):
        for img in i[2]:
            time.sleep(int(os.environ['PHOTO_PUBLISH_PERIOD']))
            publish_photo(os.fspath(Path(IMG_FOLDER_NAME) / img),
                          telegram_token,
                          chat_id)
            logging.info(f'Опубликовано фото {img}')


if __name__ == '__main__':
    main()
