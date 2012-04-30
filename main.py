#Software Design and Documentation
#Spring 2012

from __future__ import division
import pygame, sys, random
from miniGame import MiniGame
from lineGame import LineGame
from flipGame import FlipGame
from guideLoader import GuideLoader
from SGDownloader import SGDownloader
from scoreScreen import ScoreScreen
from invadersGame import InvadersGame
from highscoresList import HighscoresList
from SGUploader import SGUploader

random.seed()
#Global Variables
#screenSize = (1280, 960)
screenSize = (800, 600)
fpsLimit = 30
loaderText = ["Line Game", "Memory Cards", "Trivia Invaders", "Load Guide", "Download", "Upload"]

#Main Menu Player Avatar
#Probably should make this inherit from the actor class...
class Avatar(object):
    
    __velocity = (800, 800)
    __res = (50,50)
    
    def __init__(self, pos):
        """Makes an avatar for menu selection."""
        self.rect = pygame.Rect((0,0), self.__res)
        #self.surf = pygame.Surface((self.rect.width, self.rect.height))
        self.setPos(pos)
        self.state = {"left":False, "right":False, "up":False, "down":False}
        #Alter sprite pathing and use subsurfaces when sprite sheets are made
        self.sprite = pygame.image.load("gfx/redSquare.png").convert_alpha()
        
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
        
class LoaderBox(object):

    __res = (150, 50)
    
    def __init__(self, pos, id, text, rotation = 0):
        """Create a box to load a menu/game."""
        if rotation == 90 or rotation == 270:
            self.rect = pygame.Rect((0,0), (self.__res[1], self.__res[0]))
        else:
            self.rect = pygame.Rect((0,0), self.__res)
        self.setPos(pos)
        self.sprite = pygame.image.load("gfx/loaderBox.png").convert_alpha()
        self.font = pygame.font.SysFont("Courier", 16)
        
        self.fontSurf = self.font.render(text, False, (0,0,0))
        self.rotation = rotation
        self.res = self.__res
        self.id = id     
        
        if not self.rotation == 0:
            self.sprite = pygame.transform.rotate(self.sprite, self.rotation)
            self.res = (self.__res[1], self.__res[0])
        
    def setPos(self, pos):
        self.rect.topleft = pos
    
    def getPos(self):
        return self.rect.topleft
    
    def getRes(self):
        return self.res
    
    def getId(self):
        return self.id
        
        
    def update(self, deltaTime):
        pass
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left + self.rect.width/2.0 - self.fontSurf.get_rect().width/2.0, self.rect.top + self.rect.height/2.0 - self.fontSurf.get_rect().height/2.0),
        self.fontSurf.get_rect())
    

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
        
        self.loaderBoxes = []
        self.curLoaderId = 0
        self.avatar = False
        self.createGUI()
        self.guideMenu = False
        self.guideData = []
        
        self.loadMenu = False
        self.scoreScreen = False
        self.highscoresList = False
        
        self.lastScore = 0
        
        #lots of other stuff will be needed, of course
        #debug stuff below
        #turning off this for GUI stuff
        #self.miniGame = LineGame([])
    
    def createGUI(self):
    
        self.avatar = Avatar(((self.screen.get_width() / 2), self.screen.get_height() / 2))
        self.avatar.setPos((self.avatar.getPos()[0] - self.avatar.getRes()[0] / 2, self.avatar.getPos()[1] - self.avatar.getRes()[1] / 2))
        
        self.curLoaderId = 0
        #top loaders
        for i in range(3):
            tempBox = LoaderBox(((self.screen.get_width() / 3) * i, 0), self.curLoaderId, loaderText[self.curLoaderId])
            self.curLoaderId += 1
            tempBox.setPos((tempBox.getPos()[0] + tempBox.getRes()[0] / 3, tempBox.getPos()[1]))
            self.loaderBoxes.append(tempBox)
            
        #bottom loaders
        for i in range(3):
            tempBox = LoaderBox(((self.screen.get_width() / 3) * i, self.screen.get_height()), self.curLoaderId, loaderText[self.curLoaderId])
            self.curLoaderId += 1
            tempBox.setPos((tempBox.getPos()[0] + tempBox.getRes()[0] / 3, tempBox.getPos()[1] - tempBox.getRes()[1]))
            self.loaderBoxes.append(tempBox)    
        
        #side loaders
        #left
        #tempBox = LoaderBox((0, self.screen.get_height() / 2), self.curLoaderId, 90)
        #self.curLoaderId += 1
        #tempBox.setPos((tempBox.getPos()[0], tempBox.getPos()[1] - tempBox.getRes()[1] / 2))
        #self.loaderBoxes.append(tempBox)  
        
        #right
        #tempBox = LoaderBox((self.screen.get_width(), self.screen.get_height() / 2), self.curLoaderId, 90)
        #self.curLoaderId += 1
        #tempBox.setPos((tempBox.getPos()[0] - tempBox.getRes()[0], tempBox.getPos()[1] - tempBox.getRes()[1] / 2))
        #self.loaderBoxes.append(tempBox)
        
        #print len(self.loaderBoxes)
        
    def process_events(self):
        """Process the event queue, take in player input."""
        #lots of other stuff will be needed, of course
        run = True
        if self.miniGame:
            if not self.miniGame.process_events():
                self.lastScore = self.miniGame.get_score()
                self.scoreScreen = ScoreScreen(screenSize, self.miniGame.get_game(), self.lastScore)
                self.miniGame = False
                pygame.display.set_caption("Giga-Bright presents:")
                #self.createGUI()
        elif self.scoreScreen:
            if not self.scoreScreen.process_events():
                self.highscoresList = HighscoresList(screenSize, self.scoreScreen.get_game())
                self.scoreScreen = False
                pygame.display.set_caption("Giga-Bright presents:")
        elif self.highscoresList:
            if not self.highscoresList.process_events():
                self.highscoresList = False
                self.createGUI()
                pygame.display.set_caption("Giga-Bright presents:")
        elif self.guideMenu:
            if not self.guideMenu.process_events():
                self.guideData = self.guideMenu.retrieveData()
                #print self.guideData
                self.guideMenu = False
                self.createGUI()
                pygame.display.set_caption("Giga-Bright presents:")
        elif self.loadMenu:
            if not self.loadMenu.process_events():
                self.loadMenu = False
                self.createGUI()
                pygame.display.set_caption("Giga-Bright presents:")
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
            self.miniGame.update()
        elif self.scoreScreen:
            self.scoreScreen.update()
        elif self.highscoresList:
            self.highscoresList.update()
        elif self.guideMenu:
            self.guideMenu.update()
        elif self.loadMenu:
            self.loadMenu.update()
        else:
            self.avatar.update(delta_time)
            for l in self.loaderBoxes:
                if l.rect.colliderect(self.avatar.rect):
                    self.loadItem(l.getId())
                    pass
                    
    def draw(self):
        """Draw the game objects."""
        #call draw functions for all objects
        pygame.draw.rect(self.screen, (0,0,0), (0,0,screenSize[0],screenSize[1]))
        if self.miniGame:
            self.miniGame.draw(self.screen)
        elif self.scoreScreen:
            self.scoreScreen.draw(self.screen)
        elif self.highscoresList:
            self.highscoresList.draw(self.screen)
        elif self.guideMenu:
            self.guideMenu.draw(self.screen)
        elif self.loadMenu:
            self.loadMenu.draw(self.screen)
        else:
            self.avatar.draw(self.screen)
            for l in self.loaderBoxes:
                l.draw(self.screen)
                
    def loadItem(self, id):
        #only loading LineGame for now
        del self.loaderBoxes[:]
        del self.avatar
        #self.avatar.setPos(((self.screen.get_width() / 2), self.screen.get_height() / 2))
        #self.avatar.setPos((self.avatar.getPos()[0] - self.avatar.getRes()[0] / 2, self.avatar.getPos()[1] - self.avatar.getRes()[1] / 2))
        if id == 0:
            #debug code
            if not self.guideData:
                m = [("Question Number 1",("Answer Number 1","Ans")),\
                ("Question Number 2",("Answer Number 2","Ans")),\
                ("Question Number 3",("Answer Number 3","Ans")),\
                ("Question Number 4",("Answer Number 4","Ans")),\
                ("Question Number 5",("Answer Number 5","Ans")),\
                ("Question Number 6",("Answer Number 6","Ans")),\
                ("Question Number 7",("Answer Number 7","Ans")),\
                ("Question Number 8",("Answer Number 8","Ans"))]
                self.miniGame = LineGame(screenSize,m)
            else:
                self.miniGame = LineGame(screenSize, self.guideData)
        elif id == 1:
            self.miniGame = FlipGame(screenSize, self.guideData)
        elif id == 2:
            self.miniGame = InvadersGame(screenSize, self.guideData)
        elif id == 3:
            self.guideMenu = GuideLoader(screenSize)
        elif id == 4:
            self.loadMenu = SGDownloader(screenSize)
        elif id == 5:
            self.loadMenu = SGUploader(screenSize)
        else:
            self.createGUI()
        
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