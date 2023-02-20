import os
import requests
class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Uploaded")

    def create_folder(self, path):
        headers = self.get_headers()
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        requests.put(f'{URL}?path={path}', headers=headers)

if __name__ == '__main__':
    path_to_file = 'images/50.jpg'
    token = ''
    uploader = YandexDisk(token)
    uploader.create_folder('images')

    from glob import glob
    os.chdir('images')
    images = glob('*.jpg')
    for image in images:
        print(image, end = ' -> ')
        uploader.upload_file_to_disk(f'images/{image}', image)