import sys

from mediagrab.content import Content


def main():
    video_url = sys.argv[1]
    video = Content(video_url)
    video.download()


if __name__ == "__main__":
    main()
