import json
import logging
import sys

from django.http import HttpResponse

from .domain import bot

CHECK = 0
FOLD = -1
CALL = -2
BET  = -3
NONE = -4
SMALL_BLIND = -5
BIG_BLIND = -6
ALL_IN = -7
pykerbot = bot.PykerBot()
log = logging.getLogger('pyker')
lsh = logging.StreamHandler(sys.stdout)
lsh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
log.addHandler(lsh)
log.setLevel(logging.DEBUG)
log.info("---xxx Logging Initialized xxx---")


# Create your views here.
def init(request):
    game = request.GET
    pykerbot.init(request)
    log.debug (f"Game map is {game}")
    log.debug(f"Game is: {game['gameID']} with blinds {game['smallBlind']}/{game['bigBlind']}")
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"PykerBot"})))

def deal_hole_cards(request):
    log.info("in views.py - deal_hole_cards")
    pykerbot.deal_hole_cards(request)
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def pre_flop_bet(request):
    game = request.GET
    minimum_bet = int(game['minimumBet'])
    print (f"Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    return HttpResponse(json.dumps(dict({"amount":minimum_bet,"betType":BET,"response":""})))

def deal_flop(request):
    game = request.GET
    print (f"Flop cards are : {game.getlist('flop')}")
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def flop_bet(request):
    game = request.GET
    print (f"Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    #just fold for now.. for testing purposes.
    return HttpResponse(json.dumps(dict({"amount":0,"betType":FOLD,"response":"ok"})))
def deal_turn(request):
    return HttpResponse("Hello, you are in deal_turn. ")

def turn_bet(request):
    return HttpResponse("Hello, you are in turn_bet. ")

def deal_river(request):
    return HttpResponse("Hello, you are in deal_river. ")

def river_bet(request):
    return HttpResponse("Hello, you are in river_bet. ")

def end_hand(request):
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def end_game(request):
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))
