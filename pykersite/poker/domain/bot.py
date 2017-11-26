import logging

from .card_utilities import CardUtilities
from .bet import Bet


class PykerBot(object):
    ACE_LOW = "0A23456789XJQK"
    ACE_HIGH = "0123456789XJQKA"

    def __init__(self):
        self.log = logging.getLogger('pyker')
        self.log.debug(f"new Pykerbot Object {self} ")
        self.utils = CardUtilities()
        self.betTotal = 0


    def init(self, request):
        game = request.GET
        self.log.debug (f"Game map is {game}")
        self.smallBlind = int(game['smallBlind'])
        self.bigBlind = int(game['bigBlind'])
        self.gameID = game['gameID']
        self.log.debug(f"--->This new Pykerbot Object {self} ")
        self.quality = 0  # range 0-5
        self.log.debug(f"Game is: {self.gameID} with blinds {self.smallBlind}/{self.bigBlind}")
        self.hand = []


    def deal_hole_cards(self, request):
        game = request.GET
        self.hand = game.getlist('holeCards')
        self.log.debug (f"XXX Other players : {game.getlist('players')} hole cards are : {self.hand}")
        self.log.debug  (f'XXX  are cards suited?  {self.utils.checkHandCondition(self.hand, "suited")}')
        self.log.debug  (f'XXXX Cards Score  {self.utils.getHandValue(self.hand, "score")}')
        self.quality = self.define_hole_cards_quality()
        self.log.debug(f"Hand is {self.hand} with quality {self.quality}")

    def deal_flop(self, request):
        game = request.GET
        flop = game.getlist('flop')
        self.hand = self.hand + flop
        self.log.debug (f"Flop cards are : {flop}")
        self.quality = self.define_flop_quality()
        self.log.debug(f"Hand is {self.hand} with quality {self.quality}")

    def deal_turn(self, request):
        game = request.GET
        turn = game.getlist('turn')
        self.hand = self.hand + turn
        self.log.debug (f"Turn card is : {turn}")
        self.quality = self.define_turn_quality()
        self.log.debug(f"Hand is {self.hand} with quality {self.quality}")

    def deal_river(self, request):
        game = request.GET
        river = game.getlist('river')
        self.hand = self.hand + river
        self.log.debug (f"River card is : {river}")
        self.quality = self.define_river_quality()
        self.log.debug(f"Hand is {self.hand} with quality {self.quality}")

    def pre_flop_bet(self, request):
        return self.do_bet(request, 2.0)

    def flop_bet(self, request):
        return self.do_bet(request, 0.18)

    def turn_bet(self, request):
        return self.do_bet(request, 0.19)

    def river_bet(self, request):
        return self.do_bet(request, 0.195)

    def do_bet(self, request, round_equity_factor):
        # need a combination of hole quality.
        # since we aren't calculating actual pot odds, but a 1-5 strength evaluation of chances.. we have to go with
        # 0% chance to n% chance.  We call our
        # pot odds = our bet / (our bet + the pot)
        # having the best cards pre-flop, (i.e. AA) only gives us 80% chance of winning, so max. pot odds are 80%
        # since we have 5 strengths, for 80%, we get 0.8/5 = 0.16
        game = request.GET
        minimum_bet = int(game['minimumBet'])
        current_call = int(game['currentCall'])
        pot = int(game['pot'])
        chip_stack = int(game['chipStack'])
        self.log.debug(f"Self.quality is {self.quality}")
        card_equity = self.quality * round_equity_factor
        self.log.debug(f"---   first check  card_equity-{card_equity}, round equity factor-{round_equity_factor} and quality-{self.quality} ")

        # if cards are crap, fold. But not if you can check.
        if card_equity < 2* round_equity_factor or current_call > chip_stack:
            if (current_call == 0): # no one has bet
                return Bet.check()
            return  Bet.fold()

        # start by trying a bet..
        # we bet if the hand is strong.
        if self.quality > 2:
            if current_call == 0:
                self.log.debug(f"***  Hand of quality {self.quality} and no one has bet yet, so betting big blind")
                return self.bet_or_fold(self.bigBlind, chip_stack)
            pot_odds = (minimum_bet / (minimum_bet + pot))
            self.log.debug(f"***   Assessing bet with card_equity-{card_equity}, round equity factor-{round_equity_factor} ")
            self.log.debug(f"***       quality-{self.quality}, current call-{current_call}, pot-{pot}, pot odds-{pot_odds}")
            self.log.debug(f"***       cards are {self.hand}")
            if card_equity >= pot_odds:
                if (minimum_bet < chip_stack): # we have enough to bet.
                    return Bet.bet(minimum_bet)
                else:
                    if card_equity < 5 * round_equity_factor:
                        return Bet.fold()
                    else:
                        return Bet.all_in(chip_stack)
        else:
        # now try with a call
            if current_call == 0:
                self.log.debug(f"***  Hand of quality {self.quality} and no one has bet yet, so checking ")
                return Bet.check()
            pot_odds = (current_call / (current_call + pot))
            self.log.debug(f"***   Assessing bet with card_equity-{card_equity}, round equity factor-{round_equity_factor} ")
            self.log.debug(f"***       quality-{self.quality}, current call-{current_call}, pot-{pot}, pot odds-{pot_odds}")
            self.log.debug(f"***       cards are {self.hand}")
            if card_equity >= pot_odds:
                if current_call < chip_stack:
                    return Bet.call(current_call)
                else:
                    if card_equity < 5 * round_equity_factor:
                        return Bet.fold()
                    else:
                        return Bet.all_in(chip_stack)
            return Bet.fold()

    def define_hole_cards_quality(self):
        # break down int 1-5, 5 being the highest.
        # if
        # pair of aces, kings, queens or jacks is 5, 10-7 is 4 and any other pairs are a 3.
        if self.hand[0][0] == self.hand[1][0]:
            if any(self.hand[0][0] in c for c in 'AKQJ'):
                self.quality = 5
            elif any(self.hand[0][0] in c for c in 'X987'):
                return 4
            else:
                return 3
        # suited cards are good, too
        elif self.hand[0][1] == self.hand[1][1]:
            # QK or better
            if self.ACE_HIGH.index(self.hand[0][0]) > 11 and self.ACE_HIGH.index(self.hand[1][0]) > 11:
                return  4
            else:
                return 2
        # not suited or paired
        elif self.hand[0][0] == 'A' or self.hand[1][0] == 'A':
            return 2
        elif self.hand[0][0] == 'K' or self.hand[1][0] == 'K':
            return 2
        return 1

    def define_flop_quality(self):
        # the 5s are all the obvious ones.
        #TODO a full house is better than flush or straight, so 4 should be a lesser fullhouse score.
        if (self.utils.checkHandCondition(self.hand, "containsStraight") or
            self.utils.checkHandCondition(self.hand, "containsFlush") or
            self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
                (self.utils.checkHandCondition(self.hand, "containsFullHouse") and
                     self.utils.getHandValue(self.hand, "scoreFullHouse" > 140))):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
                self.utils.checkHandCondition(self.hand, "containsTwoPairs") or
            self.utils.checkHandCondition(self.hand, "containsOpenEndedStraight") or
                self.utils.checkHandCondition(self.hand, "maxSuitCount") == 3):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsGutShotStraight") or
                (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
            self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304)):
            return 3

        if (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) < 2305):
            return 2

        return 1  # it is a folder...

    def define_turn_quality(self):
        # the 5s are all the obvious ones.
        if ((self.utils.checkHandCondition(self.hand, "containsStraight") and
                self.utils.checkHandCondition(self.hand, "containsFlush")) or
                self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
                (self.utils.checkHandCondition(self.hand, "containsFullHouse") and (self.utils.getHandValue(self.hand, "scoreFullHouse") > 140))):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
                self.utils.checkHandCondition(self.hand, "containsTwoPairs") or
            self.utils.checkHandCondition(self.hand, "containsFlush")):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsStraight" or
            self.utils.checkHandCondition(self.hand, "containsOpenEndedStraight" or
            self.utils.checkHandCondition(self.hand, "maxSuitCount") == 3 or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304)))):
            return 3

        if (self.utils.checkHandCondition(self.hand, "containsGutShotStraight") or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                    self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) < 2305)):
            return 2

        return 1  # it is a folder...


    def define_river_quality(self):

        if (self.utils.checkHandCondition(self.hand, "containsStraight") or
                 self.utils.checkHandCondition(self.hand, "containsFlush")):
            return 5

        if (self.utils.checkHandCondition(self.hand, "containsFourOfAKind") or
                self.utils.checkHandCondition(self.hand, "containsFullHouse")):
            return 4

        if (self.utils.checkHandCondition(self.hand, "containsThreeOfAKind") or
                self.utils.checkHandCondition(self.hand, "containsTwoPairs") or
                self.utils.checkHandCondition(self.hand, "containsFlush")):
            return 3

        if (self.utils.checkHandCondition(self.hand, "containsStraight" or
            (self.utils.checkHandCondition(self.hand, "exactlyOnePair") and
                     self.utils.getHandValue(self.hand, "scoreNOfAKind", value=2) > 2304))):
            return 2

        return 1  # it is a folder...

    def call_or_fold(self, amount, chip_stack):
        if amount < chip_stack:
            return Bet.call(amount)
        if amount >= chip_stack:
            return Bet.fold()
    def bet_or_fold(self, amount, chip_stack):
        if amount < chip_stack:
            return Bet.bet(amount)
        if amount >= chip_stack:
            return Bet.fold()

    def call_or_go_all_in(self, amount, chip_stack):
        if amount < chip_stack:
            return Bet.call(amount)
        return Bet.all_in(amount)

    def bet_or_go_all_in(self, amount, chip_stack):
        if amount < chip_stack:
            return Bet.bet(amount)
        return Bet.all_in(amount)