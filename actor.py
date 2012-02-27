
import pygame

#update, draw, etc. should be defined for individual actor types
class Actor(object):
    def __init__(self):
        """initiate the actor"""
        self.rect = pygame.Rect(0,0,0,0)