import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
PATH = "/home/ekn/Downloads/chromedriver-linux64/chromedriver.exe"
service = Service(executable_path=PATH)

wd = webdriver.Chrome(options=options)

def get_images_from_google(wd, delay, max_images, name):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = f"https://yandex.com/images/search?from=tabbar&text={name}"
    wd.get(url)

    downloaded_urls_file = "downloaded_urls.txt"
    image_urls = set()

    if os.path.exists(downloaded_urls_file):
        with open(downloaded_urls_file, "r") as f:
            for line in f:
                image_urls.add(line.strip())

    images = wd.find_elements(By.CSS_SELECTOR, "img[src*='//avatars.']")

    count = 0
    for image in images:
        if count >= max_images:
            break

        if image.get_attribute('src') in image_urls:
            continue

        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
            image_urls.add(image.get_attribute('src'))
            print(f"Found {len(image_urls)}")
            print(image.get_attribute('src'))

            download_image("imgs/", image.get_attribute('src'), f"{count}_{name}.jpg")
            with open(downloaded_urls_file, "a") as f:
                f.write(image.get_attribute('src') + "\n")

            count += 1

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

names = ["cat", "dog", "bird"]  
for name in names:
    urls = get_images_from_google(wd, 3, 3, name)

wd.quit()
