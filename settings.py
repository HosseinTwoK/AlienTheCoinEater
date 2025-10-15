import pygame
from os import path
from sys import exit
from random import randint
from pygame.locals import *


SC_WIDTH = 800
SC_HEIGHT = 600
SC_SIZE = (SC_WIDTH,SC_HEIGHT)

TITLE_MENU = "Alien the Coin Eater"

FPS = 60

# center of the page
CENTER_WIDTH = SC_WIDTH//2
CENTER_HEIGHT = SC_HEIGHT//2

# colors
DARK_BLUE = (27,25,39)
DARK_RED = (100,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
YELLOW = (200,200,0)
GREEN = (0,255,0)



# player setting
PLAYER_LIVES = 5
PLAYER_STARTING_VELOCITY = 6.5
PLAYER_ACCELERATION = 0.18

# coin setting
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.18 

BUFFER_DISTACNE = 100 