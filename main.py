import argparse
from package.index import Downloader

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--u', type=str, help='url address of track')
    parser.add_argument('-S', action='store_true', help='has the video timestamps in proper format?')
    args = parser.parse_args()
    print(args)

    downloader: Downloader = Downloader(args.u, args.S)
    downloader.download()
