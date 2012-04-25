
import pygame

#a line class of some sort should be defined

class MiniGame(object):
    def __init__(self, screenSize, material):
        """Initiate the mini-game, material should be a list of question, answer tuples."""
        #hold objects here
        self.screenSize = screenSize;
        self.material = material
        self.materialCopy = [(x[0],x[1],0) for x in material]
        self.objects = []
        
    def process_events(self):
        """Process the event queue, take in player input for the mini-game."""
        #this should probably be completely redefined for each mini game
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        return run
        
    def update(self):
        """Update the game objects held by the mini-game."""
        #you'll also need to update other things that matter, of course
        for o in self.objects:
            o.update()
        
    def draw(self, screen):
        """Draw the game objects held by the mini-game."""
        #you'll also need to draw other things that matter, of course
        for o in self.objects:
            o.draw(screen)
    
    def get_score(self):
        return 0