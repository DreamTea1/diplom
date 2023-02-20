import vk
import ya
import os
from glob import glob

user_id = input('Введите user_id: ')
token = input('Введите token с ПОЛИГОНА: ')
# access_token = input('Введите token с ВК!')
access_token = ''

count_images = 5
photo_urls_likes_and_date = vk.get_urls_likes_size_and_dates(access_token, user_id)
vk.get_photo_by_urls_likes_and_dates(photo_urls_likes_and_date, 'images', count_images)

uploader = ya.YandexDisk(token)
uploader.create_folder('images')
os.chdir('images')
images = glob("*.jpg")
for image in images:
    print(image, end=' -> ')
    uploader.upload_file_to_disk(f'images/{image}', image)