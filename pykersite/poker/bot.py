
import logging
from . import card_utilities

class PykerBot(object):

    def __init__(self):
        self.log = logging.getLogger('pyker')
        self.utils = card_utilities.CardUtilities()

    def deal_hole_cards(self, request):
        game = request.GET
        self.hand = game.getlist('holeCards')
        print (f"XXX Other players : {game.getlist('players')} hole cards are : {self.hand}")
        print (f'XXX  are cards suited?  {self.utils.checkHandCondition(self.hand, "suited")}')
        print (f'XXXX Cards Score  {self.utils.getHandValue(self.hand, "score")}')

    def defineHoleCardsQuality(self):
        handQuality=0
        self.log.info(f"myHand is ${self.hand} which is of type ${type(self.hand)}")
        if (self.utils.checkHandCondition(self.hand, "suited")):
            handQuality = 1
            self.log.info(f"Logging, we are logging.. {self.hand}")



    '''
    if (utilities.containsValue(myHand,'A')||utilities.containsValue(myHand,'K')) {
    handQuality = 1
    }
    if (((utilities.containsValue(myHand,'A')||utilities.containsValue(myHand,'K')||utilities.containsValue(myHand,'Q'))) && (utilities.isSuited(myHand)))  {
    handQuality = 2 // pocket pairs above 7s or suited cards above 10/8
    }
    if (utilities.hasExactlyOnePair(myHand) && (utilities.containsValue(myHand,'A')||utilities.containsValue(myHand,'K')||utilities.containsValue(myHand,'Q')||utilities.containsValue(myHand,'J'))) {
    handQuality = 2 // pocket pairs with King or Ace
    }
    return handQuality
    }
        '''