import pygame
from highscore import retrieveHighscores


class Button(object):
    
    __offsets = (10, 3)
    
    def __init__(self, pos, text, res, id):
        """One button for choosing things"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 20)
        self.fontSurf = self.font.render(text, False, (0,0,0))
        self.sprite = pygame.image.load("gfx/button.png").convert_alpha()
        self.id = id
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left + self.__offsets[self.id], self.rect.top + self.rect.height / 2.0 - self.fontSurf.get_rect().height / 2.0), self.fontSurf.get_rect())
        
    def clickCheck(self, pos):
        return self.rect.collidepoint(pos)
        
    def getID(self):
        return self.id

class LineItem(object):
    
    
    def __init__(self, pos, text, res, id):
        """One highscore line item"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 20)
        #temp = text.replace("xml/", "")
        self.fontSurf = self.font.render(text[0] + " : " + str(text[1]), False, (0,0,0))
        self.sprite = pygame.image.load("gfx/lineItem.png").convert_alpha()
        self.id = id
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left, self.rect.top), self.fontSurf.get_rect())
        
        
    def getID(self):
        return self.id
        

class HighscoresList(object):
    
    __res = (800,600)
    __lineItemRes = (600, 20)
    __button_res = (100,75)
    __separationLine = 5
    
    
    def __init__(self, screenSize, game):
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/scoreScreen.png").convert_alpha()
        self.font = pygame.font.SysFont("Courier", 32)
        self.fontSurf = self.font.render("HIGHSCORES", False, (0,0,0))
        #self.scoreSurf = self.font.render(str(score), False, (0,0,0))
        
        self.screenSize = screenSize
        self.game = game
        
        self.scores = retrieveHighscores(self.game)
        #print self.scores
        self.button = Button((self.rect.right / 2.0 - self.__button_res[0] / 2.0, self.rect.bottom - self.__res[1] * 1.0/15.0 - self.__button_res[1]), "Done", self.__button_res, 0)
        
        self.lineItems = []
        maxItems = 0
        if len(self.scores) > 10:
            maxItems = 10
        else:
            maxItems = len(self.scores)
        for i in range(0, maxItems):
            if i == 0:
                 self.lineItems.append(LineItem((self.rect.topleft[0] + self.rect.width/2.0 - self.__lineItemRes[0] /2.0,
                 self.rect.topleft[1] + self.__res[1] * 2.0/15.0), 
                 self.scores[i], (self.__lineItemRes[0], self.__lineItemRes[1]), i))
            else:
                self.lineItems.append(LineItem((self.rect.topleft[0] + self.rect.width/2.0 - self.__lineItemRes[0] /2.0,
                self.rect.topleft[1] + self.__res[1] * 2.0/15.0 +  self.__lineItemRes[1] * i + self.__separationLine * i),
                self.scores[i], (self.__res[0], self.__lineItemRes[1]), i))
        
                
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.right / 2 - self.fontSurf.get_rect().width / 2.0, self.rect.top + self.__res[1] / 15), self.fontSurf.get_rect())
        for l in self.lineItems:
            l.draw(screen)
        self.button.draw(screen)
        
    def update(self):
        pass
        
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                    if(self.button.clickCheck(event.pos)):
                        run = False
                        
        return run
        
        
        