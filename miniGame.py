
import pygame

class MiniGame(object):
    def __init__(self):
        """Initiate the mini-game."""
        #hold miscellaneous objects here if they don't care about processing events
        objects = []
        
    def process_events(self, run):
        """Process the event queue, take in player input for the mini-game."""
        #this should probably be completely redefined for each mini game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
    def update(self):
        """Update the game objects held by the mini-game."""
        #you'll also need to update other things that matter, of course
        for o in objects:
            o.update
        
    def draw(self, screen):
        """Draw the game objects held by the mini-game."""
        #you'll also need to draw other things that matter, of course
        for o in objects:
            o.draw(screen)