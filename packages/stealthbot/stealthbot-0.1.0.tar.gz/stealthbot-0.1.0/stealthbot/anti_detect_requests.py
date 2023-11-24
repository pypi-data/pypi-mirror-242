from cloudscraper import CloudScraper
from parsel import Selector


# Create a subclass of CloudScraper
class AntiDetectRequests(CloudScraper):

    def parsel(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)

        if response.status_code == 200:
            return Selector(response.text)
        else:
            response.raise_for_status()
