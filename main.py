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
    '''
    img_folder = 'images'
    Path(img_folder).mkdir(parents=True, exist_ok=True)
    
    filename = 'hubble.jpeg'
    file_path = Path(img_folder) / (filename)
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    download_image(url, file_path)
    '''
    for img in get_latest_launch_images():
        print(img)

if __name__ == '__main__':
    main()