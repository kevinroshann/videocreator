import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_images_from_google(wd, delay, max_images, name):
    url = f"https://www.google.com/search?q={name}+images&tbm=isch"
    wd.get(url)

    downloaded_urls_file = f"downloaded_urls_{name}.txt"  # File to store downloaded URLs
    image_urls = set()

    if os.path.exists(downloaded_urls_file):
        with open(downloaded_urls_file, "r") as f:
            for line in f:
                image_urls.add(line.strip())

    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        for img in thumbnails:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CSS_SELECTOR, "img[src*='.jpg']")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    continue

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
                    print(image.get_attribute('src'))

                    # Download the image and update downloaded URLs file
                    download_image("imgs/", image.get_attribute('src'), str(len(image_urls)) + f"_{name}.jpg")
                    with open(downloaded_urls_file, "a") as f:
                        f.write(image.get_attribute('src') + "\n")

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


options = Options()
PATH = "/home/ekn/Downloads/chromedriver-linux64/chromedriver.exe"
service = Service(executable_path=PATH)
wd = webdriver.Chrome(options=options)

names = ["cat", "dog", "bird"]  # List of names to search for images
for name in names:
    urls = get_images_from_google(wd, 3, 3, name)  # Change max_images to your desired limit
    for i, url in enumerate(urls):
        download_image("imgs/", url, str(i) + f"_{name}.jpg")

wd.quit()
