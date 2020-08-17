import re, os, sys, pprint, shutil
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment
from .utils import to_seconds, download_image


def main():
    url = sys.argv[1]
    yt = YouTube(url)
    author = yt.author
    title = yt.title
    os.mkdir('./tmp')
    try:
        splitable = bool(sys.argv[2])
    except IndexError:
        splitable = None
    download_dir = './tmp' if splitable else './downloads'
    cover = download_image(yt.thumbnail_url, './tmp')


    mp4_file = yt.streams.filter(file_extension='mp4').first().download(output_path=download_dir)
    file, extension = os.path.splitext(mp4_file)
    mp3_file = file+'.mp3'

    videoClip = VideoFileClip(mp4_file)
    audioclip = videoClip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoClip.close()
    os.remove(mp4_file)

    timestamps = []
    if splitable:
        title = title.replace('/', '|')
        os.mkdir('./downloads/'+title)
        desc = yt.description.splitlines()
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
        print(mp3_file)
        whole = AudioSegment.from_mp3(mp3_file)
        for index in range(len(timestamps)):
            try:
                start = timestamps[index]['time']*1000
                end = timestamps[index + 1]['time']*1000
                song = whole[start:end]
            except IndexError:
                start = timestamps[index]['time']*1000
                end = whole.duration_seconds*1000
                song = whole[start:end]

            song.export(
                'downloads/'+title+'/'+timestamps[index]['name']+'.mp3',
                format='mp3',
                tags={
                    'artist': author,
                    'album': title
                },
                cover=cover
            )
    shutil.rmtree('./tmp')
