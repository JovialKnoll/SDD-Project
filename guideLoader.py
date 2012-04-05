import pygame
from gbxml import listXMLFiles


class LineItem(object):
    
    
    def __init__(self, pos, text, res):
        """One study guide line item"""
        self.rect = pygame.Rect((pos[0], pos[1]), res)
        self.font = pygame.font.SysFont("Courier", 20)
        self.fontSurf = self.font.render(text, False, (0,0,0))
        self.sprite = pygame.image.load("gfx/lineItem.png").convert_alpha()
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left, self.rect.top), self.fontSurf.get_rect())
        



class GuideLoader(object):
    
    __res = (600, 400)
    __lineItemOffset = 20
    __separationLine = 5
    
    def __init__(self, screenSize):
        """Study guide loader menu"""
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/guideLoader.png").convert_alpha()
        self.files = listXMLFiles()
        self.lineItems = []
        for i in range(0, len(self.files)):
            if i == 0:
                 self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1]), self.files[i], (self.__res[0], self.__lineItemOffset)))
            else:
                self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1] +  self.__lineItemOffset * i + self.__separationLine), self.files[i], (self.__res[0], self.__lineItemOffset)))
        
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        for l in self.lineItems:
            l.draw(screen)
            
        
    
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        return run