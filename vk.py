import requests
import os
from datetime import date
import json
# access_token = ''
# user_id = data.user_id
# user_id = input()

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version, 'album_id':'profile', 'extended':1}

   def users_photo(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params, })
       return response.json()

def get_json_file(list_for_json):
    with open('data.json', 'w') as f:
        json.dump(list_for_json, f, indent=2, ensure_ascii=False)

def get_urls_likes_size_and_dates(access_token, user_id):
    photo_param = {}
    vk = VK(access_token, user_id)
    items = vk.users_photo()['response']['items']
    for photo_info in items:
        photo_info['sizes'] = photo_info['sizes'][-1]
        photo_param[photo_info['id']] = {}
        photo_param[photo_info['id']]['url'] = photo_info['sizes']['url']
        photo_param[photo_info['id']]['likes'] = photo_info['likes']['count']
        photo_param[photo_info['id']]['date'] = photo_info['date']
        photo_param[photo_info['id']]['size'] = photo_info['sizes']['type']
    return photo_param

def get_photo_by_urls_likes_and_dates(photo_urls_and_likes: dict, folder_name: str='images', count_images: int = 5):
    list_for_json = []
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    for photo_id in photo_urls_and_likes:
        photo_info = photo_urls_and_likes[photo_id]
        p = requests.get(photo_info['url'])
        if os.path.exists(f"{folder_name}\{photo_info['likes']}.jpg"):
            with open(f"{folder_name}\{photo_info['likes']}-{date.fromtimestamp(photo_info['date'])}.jpg", "wb") as out:
                out.write(p.content)
                list_for_json.append({'size' : photo_info['size'], 'file_name' : f"{photo_info['likes']}-{date.fromtimestamp(photo_info['date'])}.jpg"})
                print(f"{photo_info['likes']}-{date.fromtimestamp(photo_info['date'])}.jpg downloaded")
        else:   
            with open(f"{folder_name}\{photo_info['likes']}.jpg", "wb") as out:
                out.write(p.content)
                list_for_json.append({'size' : photo_info['size'], 'file_name' :f"{photo_info['likes']}.jpg"})
                print(f"{photo_info['likes']}.jpg downloaded")
        if len(os.listdir(path="images")) == count_images:
            get_json_file(list_for_json)
            return
    get_json_file(list_for_json)