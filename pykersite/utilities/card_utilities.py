
import json
import urllib.request


class CardUtilities():
    json_result = None
    url = None

    def refreshIfNeeded(self, url):
        if self.url != url:
            res = urllib.request.urlopen(url)
            dec = res.read().decode('utf-8')
            self.json_result = json.loads(dec)
            self.url = url
        'now we have updated hand data if necessary


    def isSuited(self, url):
        self.refreshIfNeeded(url)
        return self.json_result["suited"]

