import re, os, sys, pprint, shutil
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment
from .utils import to_seconds, download_image


class Downloader:
    def __init__(self, url: str, splitable: bool):
        self.yt = YouTube(url)
        self.splitable = splitable

    def download(self):
        os.mkdir('./tmp')
        download_dir = './tmp' if self.splitable else './downloads'
        cover = download_image(self.yt.thumbnail_url, './tmp')
        author = self.yt.author
        title = self.yt.title

        mp4_file = self.yt.streams.filter(file_extension='mp4').first().download(output_path=download_dir)
        audio = AudioSegment.from_file(mp4_file)

        if self.splitable:
            self.split(audio, title, author, cover)
        else:
            audio.export(
                'downloads/' + title + '.mp3',
                format='mp3',
                tags={
                    'artist': author,
                    'album': title
                },
                cover=cover
            )

        os.remove(mp4_file)
        shutil.rmtree('./tmp')

    def split(self, audio_file, title, author, cover):
        timestamps = []
        safe_title = title.replace('/', '|')
        os.mkdir('./downloads/' + safe_title)
        desc = self.yt.description.splitlines()
        for line in desc:
            if re.search('[0-9]{1,2}:[0-9]{2}', line):
                time, name = line.split(' ', 1)

                if time[0] == '[':
                    time = time[1:len(time)]
                if time[len(time) - 1] == ']':
                    time = time[0:len(time) - 1]

                time = to_seconds(time)

                data = {
                    'time': time,
                    'name': name
                }
                timestamps.append(data)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(timestamps)
        for index in range(len(timestamps)):
            try:
                start = timestamps[index]['time'] * 1000
                end = timestamps[index + 1]['time'] * 1000
                song = audio_file[start:end]
            except IndexError:
                start = timestamps[index]['time'] * 1000
                end = audio_file.duration_seconds * 1000
                song = audio_file[start:end]

            song.export(
                'downloads/' + safe_title + '/' + timestamps[index]['name'] + '.mp3',
                format='mp3',
                tags={
                    'artist': author,
                    'album': safe_title
                },
                cover=cover
            )
