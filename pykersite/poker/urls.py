from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^initGame$', views.init, name='init'),
    url(r'^dealHoleCards', views.deal_hole_cards, name='deal_hole_cards'),
    url(r'^preFlopBet', views.pre_flop_bet, name='pre_flop_bet'),
    url(r'^dealFlop', views.deal_flop, name='deal_flop'),
    url(r'^flopBet', views.flop_bet, name='flop_bet'),
    url(r'^dealTurn', views.deal_turn, name='deal_turn'),
    url(r'^turnBet', views.turn_bet, name='turn_bet'),
    url(r'^dealRiver', views.deal_river, name='deal_river'),
    url(r'^riverBet', views.river_bet, name='river_bet'),
    url(r'^endHand', views.end_hand, name='end_hand'),
    url(r'^endGame', views.end_game, name='end_game')
]