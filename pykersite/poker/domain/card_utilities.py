
import json
from urllib import request
from urllib import parse
from django.conf import settings

class CardUtilities(object):
    json_result = None
    hand = None
    value =-1

    def refreshIfNeeded(self, p_hand, p_value=-1):
        if CardUtilities.hand != p_hand or CardUtilities.value != p_value:
            util_url = self.constructUrl(p_hand, p_value)
            res = request.urlopen(util_url)
            dec = res.read().decode('utf-8')
            CardUtilities.json_result = json.loads(dec)
            CardUtilities.hand = p_hand
            CardUtilities.value = p_value

            # now we have updated hand data if necessary

    def constructUrl(self, p_hand, value):
        print (f"Trying to construct URL with {p_hand}")
        hand_tuple = tuple({('myHand',x) for x in p_hand})
        constructed_url = "http://{}?{}".format(settings.CARD_UTILITIES_BASE_URL,parse.urlencode(hand_tuple), value)
        print (f"Constructed URL is {constructed_url}")
        return constructed_url

    def checkHandCondition(self, my_hand, property, other_hand=None,  value=-1):
        self.refreshIfNeeded(my_hand, value)
        return self.json_result[property]

    def getHandValue(self, my_hand, property, other_hand=None,  value=-1):
        return self.checkHandCondition(my_hand, property, other_hand, value)



'''
{"exactlyOnePair":true,"containsValue":false,"containsTwoPairs":false,"containsThreeOfAKind":false,
"containsFlush":false,"best5CardHand":[],"containsStraight":false,"containsFourOfAKind":false,
"containsFullHouse":false,"containsStraightFlush":false,"score":920842,"scoreNOfAKind":10,"scoreTwoPairs":218,
"maxSuitCount":1,"maxConsecutives":0,"containsExactlyNSuits":false,"containsOpenEndedStraight":false,
"scoreStraight":13,"scoreFullHouse":13,"compareHands":920838,"suited":false}
'''