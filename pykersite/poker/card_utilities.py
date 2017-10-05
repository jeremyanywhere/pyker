
import json
from urllib import request
from urllib import parse
from django.conf import settings

class CardUtilities(object):
    json_result = None
    hand = None

    def refreshIfNeeded(self, p_hand):
        if CardUtilities.hand != p_hand:
            util_url = self.constructUrl(p_hand)
            res = request.urlopen(util_url)
            dec = res.read().decode('utf-8')
            CardUtilities.json_result = json.loads(dec)
            CardUtilities.hand = p_hand
            # now we have updated hand data if necessary

    def constructUrl(self, p_hand):
        print (f"Trying to construct URL with {p_hand}")
        hand_tuple = tuple({('myHand',x) for x in p_hand})
        constructed_url = "http://{}?{}".format(settings.CARD_UTILITIES_BASE_URL,parse.urlencode(hand_tuple))
        print (f"Constructred URL is {constructed_url}")
        return constructed_url


    def isSuited(self, hand):
        self.refreshIfNeeded(hand)
        return self.json_result["suited"]

