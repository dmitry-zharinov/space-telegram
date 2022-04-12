import requests
from pathlib import Path


IMG_FOLDER_NAME = 'images'

def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v5/launches/')
    response.raise_for_status()
    images = response.json()[12]['links']['flickr']['original']
    for img_number, img_url in enumerate(images):
        download_image(img_url, Path(IMG_FOLDER_NAME) / (f'spacex{img_number}.jpg'))
        
        
def main():
    
    Path(IMG_FOLDER_NAME).mkdir(parents=True, exist_ok=True)
    '''
    filename = 'hubble.jpeg'
    file_path = Path(img_folder) / (filename)
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    download_image(url, file_path)
    '''
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()