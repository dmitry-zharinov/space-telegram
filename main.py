import requests
from pathlib import Path

def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(path, 'wb') as file:
        file.write(response.content)


def main():
    filename = 'hubble.jpeg'
    img_folder = 'images'
    
    Path(img_folder).mkdir(parents=True, exist_ok=True)
    file_path = Path(img_folder) / (filename)
    
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    
    download_image(url, file_path)

if __name__ == '__main__':
    main()