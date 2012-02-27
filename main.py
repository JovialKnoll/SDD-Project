#Software Design and Documentation
#Spring 2012

from __future__ import division
import pygame, sys, random
from miniGame import MiniGame

random.seed()
#Global Variables
screenSize = (800, 600)
fpsLimit = 30

#Game Object
class Game(object):
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption("Giga-Bright presents:")
        self.clock = pygame.time.Clock()
        self.miniGame = False
        #lots of other stuff will be needed, of course
        
    def process_events(self):
        """Process the event queue, take in player input."""
        #lots of other stuff will be needed, of course
        run = True
        if self.miniGame:
            miniGame.process_events(run)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
        return run
        
    def update(self):
        """Update the game objects."""
        #call update functions for all objects
        if self.miniGame:
            miniGame.process_events()
        else:
            pass
        
    def draw(self):
        """Draw the game objects."""
        #call draw functions for all objects
        if self.miniGame:
            self.miniGame.draw(self.screen)
        else:
            pass
        
def main():
    g = Game()
    run = True
    while run:
        g.clock.tick(fpsLimit)
        run = g.process_events()
        g.update()
        g.draw()
        pygame.display.flip()
        
    sys.exit()
    
if __name__ == "__main__":
    main()