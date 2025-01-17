import os
from abc import ABC

from webdriver_manager.core.http import WDMHttpClient
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import File, split_ext


class DownloadManager(ABC):
    def __init__(self, http_client):
        self._http_client = http_client

    def download_file(self, url: str) -> File:
        raise NotImplementedError

    @property
    def http_client(self):
        return self._http_client


class WDMDownloadManager(DownloadManager):
    def __init__(self, http_client=None):
        if http_client is None:
            http_client = WDMHttpClient()
        super().__init__(http_client)

    def download_file(self, url: str) -> File:
        log(f"About to download new driver from {url}")
        response = self._http_client.get(url)
        ext = split_ext(url)[1]
        if ext.lower() not in (".zip", ".tar.gz", ".deb"):
            ext = split_ext(url, max_separators=2)[1]

        log(f"Driver downloading response is {response.status_code}")
        file_name = self.extract_filename_from_url(url)
        return File(response, file_name, ext)

    @staticmethod
    def extract_filename_from_url(url):
        # Split the URL by '/'
        url_parts = url.split('/')
        # Get the last part of the URL, which should be the filename
        filename = url_parts[-1]
        # Decode the URL-encoded filename
        filename = os.path.basename(filename)
        return filename