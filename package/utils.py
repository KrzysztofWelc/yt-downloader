import requests
from os.path import splitext, abspath


def to_seconds(timestamp):
    time = timestamp.split(':')

    if len(time) == 2:
        minutes = int(time[0]) * 60
        seconds = int(time[1])
        return minutes + seconds

    if len(time) == 3:
        hours = int(time[0]) * 60 * 60
        minutes = int(time[1]) * 60
        seconds = int(time[2])
        return hours + minutes + seconds


def download_image(url, output_path):
    r = requests.get(url, allow_redirects=True)
    filename, ext = splitext(url.rsplit('?')[0])
    path = output_path+'/cover'+ext
    open(path, 'wb').write(r.content)
    return abspath(path)
