import requests
from pathlib import Path

def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(path, 'wb') as file:
        file.write(response.content)


def get_latest_launch_images():
    response = requests.get('https://api.spacexdata.com/v5/launches/')
    response.raise_for_status()
    return response.json()[12]['links']['flickr']['original']

def main():
    img_folder = 'images'
    Path(img_folder).mkdir(parents=True, exist_ok=True)
    '''
    filename = 'hubble.jpeg'
    file_path = Path(img_folder) / (filename)
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    download_image(url, file_path)
    '''
    for img_number, img_url in enumerate(get_latest_launch_images()):
        download_image(img_url, Path(img_folder) / (f'spacex{img_number}.jpg'))

if __name__ == '__main__':
    main()