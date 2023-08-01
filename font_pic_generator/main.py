import requests
import os

from PIL import Image, ImageDraw, ImageFont

def create_font_preview(font_name):
    text = "Aa"

    image_width = 100
    image_height = 100

    url = f"https://fonts.googleapis.com/css2?family={font_name.title().replace(' ', '+')}"
    response = requests.get(url)

    if response.status_code != 200:
        print('\n\n', font_name, ' \n\n')
        return
    q = response.text[response.text.find('src:') + 9:]
    font_url = q[:q.find(') format')]

    font_file = requests.get(font_url)

    with open("temp_font.ttf", "wb") as f:
        f.write(font_file.content)

    image = Image.new("RGB", (image_width, image_height), "#f5efe4")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("temp_font.ttf", size=60)
    text_width, text_height = draw.textsize(text, font=font)
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2

    draw.text((x, y), text, font=font, fill="black")

    image.save(f"media/fonts/{font_name.replace(' ', '_')}.webp")
    os.remove("temp_font.ttf")


with open("font_pic_generator/font_list.txt", "r") as file:
    font_list = file.read().splitlines()


for font_name in font_list:
    create_font_preview(font_name)

    



