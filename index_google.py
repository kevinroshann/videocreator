import pathlib
import textwrap
import json
import google.generativeai as genai
from moviepy.editor import *
#scraping
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
import pyttsx3
import wave
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
padding = 50 
GOOGLE_API_KEY = 'AIzaSyB0_wgK506dJ4lCOe-ppjuj99EbrK98q_Q'

def list_files_in_folder(folder_path):
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)
    return file_names


def text_to_audio(text, output_file, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust the rate (words per minute)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

def get_audio_duration(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        frames = audio_file.getnframes()
        rate = audio_file.getframerate()
        duration = frames / float(rate)
        return duration

genai.configure(api_key=GOOGLE_API_KEY)
from IPython.display import display
from IPython.display import Markdown


topic=input("enter the topic for which you want to create video of");


def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


model = genai.GenerativeModel('gemini-pro')

chat_history = []
chat = model.start_chat(history=chat_history)





user_message=f"I need to create a youtube video on {topic} . It is about 3 minutes. so can you create a script of the audio for that documentry. I need the each script in json format. so in json format i need 'title', 'narration' and 'google_phrase' to serach of the image to put on the video on that title. I need teh text strictly in json format seperated by a comma"

chat_history.append(user_message)
response = chat.send_message(user_message)
chat_history.append(response.text)
print(to_markdown(response.text))

result = response.text.split('{', 1)
result_1=result[1].rsplit('}',1) 
result_text = '{'+result_1[0]+'},'

json_objects = result_text.split('},')
for i in json_objects:

    print(i)
    print("finish")

# Remove any leading or trailing whitespace from each JSON object
json_objects = [obj.strip() for obj in json_objects if obj.strip()]

# Parse each JSON object and append it to a list
json_list = []
for obj in json_objects:
    # Add back the '}' that was removed during the split
    obj += '}'
    json_list.append(json.loads(obj))

# Print the list of JSON objects
print(json_list)
print('---------------------------------------')
print ( json_list[0]['google_phrase'])
names=[]
title=[]
narration=[]
audio_duration=0
for i in json_list:
    names.append(i['google_phrase'])
    title.append(i['title'])
    narration.append(i['narration'])
    text=i['narration']
    # output_file = f"audio/{i['title']}.wav"  
    # text_to_audio(text, output_file, rate=150)
    # audio_duration=audio_duration+get_audio_duration(output_file)

    


    

options = Options()
PATH = "/home/ekn/Downloads/chromedriver-linux64/chromedriver.exe"
service = Service(executable_path=PATH)

wd = webdriver.Chrome(options=options)


def get_images_from_google(wd, delay, max_images, name):
    # def scroll_down(wd):
    #     wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(delay)
    
    # url = f"https://yandex.com/images/search?from=tabbar&text={name}"
    url = f"https://www.google.com/search?q={name}+images&tbm=isch"
    # url = f"https://www.bing.com/images/search?q={name}&form=HDRSC3&first=1"
    wd.get(url)

    downloaded_urls_file = "downloaded_urls.txt"
    image_urls = []
    
    if os.path.exists(downloaded_urls_file):
        with open(downloaded_urls_file, "r") as f:
            for line in f:
                image_urls.add(line.strip())

    # images = wd.find_elements(By.CSS_SELECTOR, "img[src*='//avatars.']")
    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        for img in thumbnails:
            try:
                    img.click()
                    time.sleep(delay)
            except:
                    continue
            images = wd.find_elements(By.CSS_SELECTOR, "img[src*='.jpg']")
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
                    folder_path = f"C:\\Users\\ekn\\Desktop\\github-projects\\video creator\\imgs\\{name}"

                    if not os.path.exists(folder_path):
                        print("created")
                        os.makedirs(folder_path)
                    download_image(f"imgs/{name}/", image.get_attribute('src'), f"{count}.jpg")
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


for name in names:
    urls = get_images_from_google(wd, 3, 3, name)

wd.quit()
image_clips = []

for i in json_list:
    img=[]
    text=i['narration']
    output_file = f"audio/{i['google_phrase']}.wav"  
    text_to_audio(text, output_file, rate=150)
    duration=get_audio_duration(output_file)
    background_clip = ColorClip((1920, 1080), color=(255, 255, 255)).set_duration(duration)
    text_clip = TextClip(text, font="Arial", fontsize=72, color='white', align='center', method='caption', size=(1920 - 2 * padding, None)).set_duration(duration)


# Get the height of the text clip
    text_height = text_clip.h
    y_position = 1080 - text_height - padding

# Position the text clip horizontally centered and at the bottom
    text_clip = text_clip.set_position(("center", y_position))


    folder_path = f"imgs/{i['google_phrase']}"  # Replace with the path to your folder
    image_paths=[]
    image_clips = []
    file_names = list_files_in_folder(folder_path)
    for file_name in file_names:
        image_paths.append(f"imgs/{i['google_phrase']}/{file_name}")
    for image_path in image_paths:
        image_clip = ImageClip(image_path, duration=duration/3).resize((1920, 1080))  # Match text duration and size
        image_clips.append(image_clip)

    composite_clip = CompositeVideoClip([
    background_clip.set_position(("center", "center")),
    *[(clip.set_position(("center", "center")).set_start(idx * 5)) for idx, clip in enumerate(image_clips)],
    text_clip
])
    # folder_path = f"C:\\Users\\ekn\\Desktop\\github-projects\\video creator\\video\\{i['title']}"

    # if not os.path.exists(folder_path):
    #     print("created")
    #     os.makedirs(folder_path)
    composite_clip.write_videofile(f"C:/Users/ekn/Desktop/github-projects/video creator/video/{i['title']}.mp4", fps=24)


# You can continue the conversation by adding new user_messages
# and calling chat_with_ai for each message


