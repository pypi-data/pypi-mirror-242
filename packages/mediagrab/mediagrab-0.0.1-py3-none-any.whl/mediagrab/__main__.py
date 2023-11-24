import sys

import pytube


def main():
    video_url = sys.argv[1]

    yt = pytube.YouTube(video_url)
    stream = yt.streams.get_highest_resolution()

    stream.download()


if __name__ == "__main__":
    main()
