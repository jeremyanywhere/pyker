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
    log.debug(f"Starting Game: {game['gameID']} with blinds {game['smallBlind']}/{game['bigBlind']}")
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"PykerBot"})))

def deal_hole_cards(request):
    log.info("->in views.py - deal_hole_cards")
    pykerbot.deal_hole_cards(request)
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def deal_flop(request):
    log.info("->in views.py - deal_flop")
    pykerbot.deal_flop(request)
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def deal_turn(request):
    log.info("->in views.py - deal_turn")
    pykerbot.deal_turn(request)
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def deal_river(request):
    log.info("->in views.py - deal_river")
    pykerbot.deal_river(request)
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def pre_flop_bet(request):
    game = request.GET
    minimum_bet = int(game['minimumBet'])
    current_call = int(game['currentCall'])
    my_pot = int(game['pot'])
    my_chip_stack = game['chipStack']
    print (f"pre-flop bet. Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    result = pykerbot.pre_flop_bet(request)
    return HttpResponse(json.dumps(result))

def flop_bet(request):
    game = request.GET
    minimum_bet = int(game['minimumBet'])
    current_call = int(game['currentCall'])
    my_pot = int(game['pot'])
    my_chip_stack = game['chipStack']
    print (f"flop bet. Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    #just fold for now.. for testing purposes.
    result = pykerbot.flop_bet(request)
    return HttpResponse(json.dumps(result))

def turn_bet(request):
    game = request.GET
    minimum_bet = int(game['minimumBet'])
    current_call = int(game['currentCall'])
    my_pot = int(game['pot'])
    my_chip_stack = game['chipStack']
    print (f"turn bet. Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    #just fold for now.. for testing purposes.
    result = pykerbot.turn_bet(request)
    return HttpResponse(json.dumps(result))

def river_bet(request):
    game = request.GET
    minimum_bet = int(game['minimumBet'])
    current_call = int(game['currentCall'])
    my_pot = int(game['pot'])
    my_chip_stack = game['chipStack']
    print (f"turn bet. Pot : {game['pot']}, my chips: {game['chipStack']}, current minimum bet : {minimum_bet}")
    #just fold for now.. for testing purposes.
    result = pykerbot.turn_bet(request)
    return HttpResponse(json.dumps(result))

def end_hand(request):
    #todo:  did I win?
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

def end_game(request):
    #todo:  did I win?
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"ok"})))

