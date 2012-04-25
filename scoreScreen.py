import pygame


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


class ScoreScreen(object):
    
    __res = (800,600)
    __button_res = (100,75)
    __button_offset = 20
    
    
    def __init__(self, screenSize, score):
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/scoreScreen.png").convert_alpha()
        self.font = pygame.font.SysFont("Courier", 32)
        self.fontSurf = self.font.render("YOUR SCORE THIS GAME WAS", False, (0,0,0))
        self.scoreSurf = self.font.render(str(score), False, (0,0,0))
        
        self.selectionIndex = -1
        self.buttons = []
        self.done = False
        
        self.buttons.append(Button((self.rect.topleft[0] + self.__button_offset, self.rect.topleft[1] + self.__res[1] * 2.0 / 3.0), "Upload", self.__button_res, 0))
        self.buttons.append(Button((self.rect.topright[0] - self.__button_offset - self.__button_res[0], self.rect.topleft[1] + self.__res[1] * 2.0 / 3.0), "Continue", self.__button_res, 1))
        
        
    def update(self):
        if self.selectionIndex == 0:
            #upload
            pass
        elif self.selectionIndex == 1:
            self.done = True
            
            
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.right / 2 - self.fontSurf.get_rect().width / 2.0, self.rect.bottom / 2), self.fontSurf.get_rect())
        screen.blit(self.scoreSurf, (self.rect.right / 2 - self.scoreSurf.get_rect().width / 2.0, (self.rect.bottom / 2) + self.fontSurf.get_rect().height), self.scoreSurf.get_rect())
        for b in self.buttons:
            b.draw(screen)
        
    def process_events(self):
        run = True
        if self.done:
            run = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    for b in self.buttons:
                            if(b.clickCheck(event.pos)):
                                self.selectionIndex = b.getID()
                        
        return run