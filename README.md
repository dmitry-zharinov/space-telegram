# space-telegram
 
Консольная утилита:
- загружает фотографии с последнего запуска SpaceX
- загружает фотографии дня [NASA Astronomy Picture of the Day](https://apod.nasa.gov/apod/astropix.html)
- загружает фотографии планеты [NASA Earth Polychromatic Imaging Camera](https://epic.gsfc.nasa.gov/)
- публикует в Telegram-канал

### Установка
1. Предварительно должен быть установлен Python3.
2. Для установки зависимостей, используйте команду pip (или pip3, если есть конфликт с Python2) :
```
pip install -r requirements.txt
```
3. Для работы с API NASA необходимо [получить токен](https://api.nasa.gov/)
4. Для публикации фотографий в Telegram, необходимо [зарегистрировать бота и получить его API-токен](https://telegram.me/BotFather)
5. В директории скрипта создайте файл `.env` и укажите в нём следующие данные:
```
NASA_API_KEY=nasa_token
TG_BOT_TOKEN=telegram_token
TG_CHAT_ID=@chat_id
PHOTO_PUBLISH_PERIOD=86400
```
Где:
- *nasa_token* - токен для работы с API NASA
- *telegram_token* - токен для Telegram-бота
- *@chat_id* - идентификатор канала в Telegram, в котором будут публиковаться фотографии
- *PHOTO_PUBLISH_PERIOD=86400* - периодичность публикаций в секундах


### Запуск
```
$ python main.py
```

### Цели проекта

Код написан в образовательных целях для курса [dvmn.org](https://dvmn.org/).