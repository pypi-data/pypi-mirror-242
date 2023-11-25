import pytube


class Content:
    def __init__(self, url: str) -> None:
        self._url = url
        self._content = pytube.YouTube(url)

    @property
    def url(self) -> str:
        return self._url

    @property
    def content(self):
        return self._content

    def download(self) -> None:
        self.content.streams.get_highest_resolution().download()
