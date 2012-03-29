#Software Design and Documentation
#Spring 2012

from __future__ import division
import pygame, sys, random
from miniGame import MiniGame

random.seed()
#Global Variables
screenSize = (800, 600)
fpsLimit = 30


#Main Menu Player Avatar
#Probably should make this inherit from the actor class...
class Avatar(object):
    
    __velocity = (200, 200)
    __res = (50,50)
    
    def __init__(self, pos):
        """Makes an avatar for menu selection."""
        self.rect = pygame.Rect((0,0), self.__res)
        #self.surf = pygame.Surface((self.rect.width, self.rect.height))
        self.setPos(pos)
        self.state = {"left":False, "right":False, "up":False, "down":False}
        
        #Alter sprite pathing and use subsurfaces when sprite sheets are made
        self.sprite = pygame.image.load("redSquare.png").convert_alpha()
        
    def setPos(self, pos):
        self.rect.topleft = pos
        
    def getPos(self):
        return self.rect.topleft
    
    def getRes(self):
        return self.__res
        
    def update(self, deltaTime):
        if self.state['left']:
            self.setPos((self.rect.topleft[0] - self.__velocity[0] * deltaTime, self.rect.topleft[1]))
        if self.state['up']:
            self.setPos((self.rect.topleft[0],  self.rect.topleft[1] - self.__velocity[1] * deltaTime))
        if self.state['right']:
            self.setPos((self.rect.topleft[0] + self.__velocity[0] * deltaTime, self.rect.topleft[1]))
        if self.state['down']:
            self.setPos((self.rect.topleft[0],  self.rect.topleft[1] + self.__velocity[1] * deltaTime))
        
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        pygame.display.flip()
        

        
class loaderBox(object):

    __res = (150, 50)
    
    def __init__(self, pos):
        """Create a box to load a menu/game."""
        self.rect = pygame.Rect((0,0), self.__res)
        self.setPos(pos)
        
        

#Game Object
class Game(object):

    __fps = 60 
     
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption("Giga-Bright presents:")
        self.clock = pygame.time.Clock()
        self.miniGame = False
        self.avatar = Avatar(((self.screen.get_width() / 2), self.screen.get_height() / 2))
        self.avatar.setPos((self.avatar.getPos()[0] - self.avatar.getRes()[0] / 2, self.avatar.getPos()[1] - self.avatar.getRes()[1] / 2))
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
                    if self.avatar:
                        if event.key == pygame.K_RIGHT:
                            self.avatar.state['right'] = True
                        if event.key == pygame.K_LEFT:
                            self.avatar.state['left'] = True
                        if event.key == pygame.K_UP:
                            self.avatar.state['up'] = True
                        if event.key == pygame.K_DOWN:
                            self.avatar.state['down'] = True
                            
                if event.type == pygame.KEYUP:
                    if self.avatar:
                        if event.key == pygame.K_RIGHT:
                            self.avatar.state['right'] = False
                        if event.key == pygame.K_LEFT:
                            self.avatar.state['left'] = False
                        if event.key == pygame.K_UP:
                            self.avatar.state['up'] = False
                        if event.key == pygame.K_DOWN:
                            self.avatar.state['down'] = False
        return run
        
    def update(self):
        """Update the game objects."""
        #call update functions for all objects
        delta_time = float(self.clock.tick(self.__fps)) / 1000
        
        if self.miniGame:
            miniGame.update()
        else:
            self.avatar.update(delta_time)
        
    def draw(self):
        """Draw the game objects."""
        #call draw functions for all objects
        if self.miniGame:
            self.miniGame.draw(self.screen)
        else:
            self.screen.fill(pygame.Color("black"))
            self.avatar.draw(self.screen)
        
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