from django.shortcuts import render
from django.http import HttpResponse
import json


CHECK = 0
FOLD = -1
CALL = -2
BET  = -3
NONE = -4
SMALL_BLIND = -5
BIG_BLIND = -6
ALL_IN = -7


# Create your views here.
def init(request):
    game = request.GET
    print (f"Game map is {game}")
    print(f"Game is: {game['gameID']} with blinds {game['smallBlind']}/{game['bigBlind']}")
    return HttpResponse(json.dumps(dict({"amount":0,"betType":0,"response":"PykerBot"})))

def deal_hole_cards(request):
    game = request.GET
    print (f"Other players : {game.getlist('players')} hole cards are : {game.getlist('holeCards')}")
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
