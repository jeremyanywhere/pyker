import logging
import sys

from . import card_utilities

ACE_LOW = "0A23456789XJQK"
ACE_HIGH = "0123456789XQKA"
CHECK = 0
FOLD = -1
CALL = -2
BET  = -3
NONE = -4
SMALL_BLIND = -5
BIG_BLIND = -6
ALL_IN = -7


class PykerBot(object):

    def __init__(self):
        self.log = logging.getLogger('pyker')
        self.utils = card_utilities.CardUtilities()
        self.betTotal = 0

    def init(self, request):
        game = request.GET
        self.log.debug (f"Game map is {game}")
        self.smallBlind = game['smallBlind']
        self.bigBlind = game['bigBlind']
        self.gameID = game['gameID']
        self.quality = 0  # range 0-?
        self.log.debug(f"Game is: {self.gameID} with blinds {self.smallBlind}/{self.bigBlind}")


    def deal_hole_cards(self, request):
        game = request.GET
        self.hand = game.getlist('holeCards')
        self.log.debug (f"XXX Other players : {game.getlist('players')} hole cards are : {self.hand}")
        self.log.debug  (f'XXX  are cards suited?  {self.utils.checkHandCondition(self.hand, "suited")}')
        self.log.debug  (f'XXXX Cards Score  {self.utils.getHandValue(self.hand, "score")}')
        self.defineHoleCardsQuality()

    def pre_flop_bet(self, ):



        return {"amount":minimum_bet,"betType":BET,"response":""}

    def defineHoleCardsQuality(self):
        # break down int 1-5, 5 being the highest.
        # if
        self.quality = 1
        # pair of aces, kings, queens or jacks is 5, 10-7 is 4 and any other pairs are a 3.
        if self.hand[0][0] == self.hand[1][0]:
            if any(self.hand[0][0] in c for c in 'AKQJ'):
                self.quality = 5
            elif any(self.hand[0][0] in c for c in 'X987'):
                self.quality = 4
            else:
                self.quality = 3
        # suited cards are good, too
        elif self.hand[0][1] == self.hand[1][1]:
            # QK or better
            if ACE_HIGH.index(self.hand[0][0]) > 11 and ACE_HIGH.index(self.hand[1][0]) > 11:
                self.quality = 4
            else:
                self.quality = 3
        # not suited or paired
        elif self.hand[0][0] == 'A' or self.hand[1][0] == 'A':
            self.quality = 3
        elif self.hand[0][0] == 'K' or self.hand[1][0] == 'K':
            self.quality = 3
        elif self.hand[0][0] == 'Q' or self.hand[1][0] == 'Q':
            self.quality = 2
        self.log.debug(f"Defining hole cards quality..{self.quality}")

    def defineFlopCardsQuality(self):
        # the 5s are all the obvious ones.
        #TODO a full house is better than flush or straight, so 4 should be a lesser fullhouse score.
        if (self.utils.checkHandCondition(self.hand, "containsStraight") or
            self.utils.checkHandCondition(self.hand, "containsFlush") or
            self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
            (self.utils.checkHandCondition(self.hand, "containsFullHouse") and self.utils.getHandValue(self.hand, "scoreFullHouse" > 140))):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
            self.utils.checkHandCondition(self.hand, "containsOpenEndedStraight")):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsGutShotStraight")  or
                (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
            self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304)):
            return 3

        if (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                         self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) < 2305):
            return 2

        return 1  # it is a folder...

    def defineTurnCardsQuality(self):
        # the 5s are all the obvious ones.
        if ((self.utils.checkHandCondition(self.hand, "containsStraight") and
                self.utils.checkHandCondition(self.hand, "containsFlush")) or
                self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
                (self.utils.checkHandCondition(self.hand, "containsFullHouse") and self.utils.getHandValue(self.hand, "scoreFullHouse" > 140))):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
            self.utils.checkHandCondition(self.hand, "containsFlush")):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsStraight" or
            self.utils.checkHandCondition(self.hand, "containsOpenEndedStraight" or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304)))):
            return 3

        if (self.utils.checkHandCondition(self.hand, "containsGutShotStraight") or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                    self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) < 2305)):
            return 2

        return 1  # it is a folder...


    def defineRiverCardsQuality(self):
        # the 5s are all the obvious ones.
        if ((self.utils.checkHandCondition(self.hand, "containsStraight") and
                 self.utils.checkHandCondition(self.hand, "containsFlush")) or
                self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
                (self.utils.checkHandCondition(self.hand, "containsFullHouse") and self.utils.getHandValue(self.hand, "scoreFullHouse" > 140))):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
                self.utils.checkHandCondition(self.hand, "containsFlush")):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsStraight" or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                     self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304))):
            return 3

        if (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                    self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) < 2305):
            return 2

        return 1  # it is a folder...
    def highestCardValue(self):
        # get the highest value card. If it is a Full House, get the highest trip.