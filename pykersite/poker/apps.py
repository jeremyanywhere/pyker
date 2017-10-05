from django.apps import AppConfig


class PokerConfig(AppConfig):
    name = 'poker'
    utilities_url = 'localhost etc'
    NANCY = 'Nancy defined here..'
    print ("Well here we are in the PokerConfig class.. maybe we should define stuff here?")
