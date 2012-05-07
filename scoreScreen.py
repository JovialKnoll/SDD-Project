import pygame
from highscore import add_score


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
        
    def click_check(self, pos):
        return self.rect.collidepoint(pos)
        
    def getID(self):
        return self.id
        
class ScorePopup(object):
    
    def __init__(self, pos, res, loaded):
        """Defines the success/fail of the operation"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 16)
        if loaded:
            self.fontSurf = self.font.render("Score uploaded successfully.", False, (0,0,0))
        else:
            self.fontSurf = self.font.render("Could upload score.", False, (0,0,0))
        self.sprite = pygame.image.load("gfx/loaderPopup.png").convert_alpha()
        
    def draw(self,screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left + self.rect.width/2.0 - self.fontSurf.get_rect().width/2.0, self.rect.top + self.rect.height/2.0 - self.fontSurf.get_rect().height/2.0),
        self.fontSurf.get_rect())
        
    def click_check(self, pos):
        return self.rect.collidepoint(pos)


class ScoreScreen(object):
    
    __res = (800,600)
    __button_res = (100,75)
    __button_offset = 20
    __popup_res = (300, 200)
    
    
    def __init__(self, screenSize, game, score):
        """Creates a screen to display the score just recieved"""
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/scoreScreen.png").convert_alpha()
        self.font = pygame.font.SysFont("Courier", 32)
        self.fontSurf = self.font.render("YOUR SCORE THIS GAME WAS", False, (0,0,0))
        self.scoreSurf = self.font.render(str(score), False, (0,0,0))
        
        self.screenSize = screenSize
        self.game = game
        self.score = score
        
        self.selectionIndex = -1
        self.buttons = []
        self.done = False
        self.scorePopup = False
        
        #buttons for uploading or continuing
        self.buttons.append(Button((self.rect.topleft[0] + self.__button_offset, self.rect.topleft[1] + self.__res[1] * 2.0 / 3.0), "Upload", self.__button_res, 0))
        self.buttons.append(Button((self.rect.topright[0] - self.__button_offset - self.__button_res[0], self.rect.topleft[1] + self.__res[1] * 2.0 / 3.0), "Continue", self.__button_res, 1))
        
        
    def update(self):
        #upload button
        if self.selectionIndex == 0:
            self.success = add_score(self.game, self.score)
            self.scorePopup = ScorePopup((self.screenSize[0]/2 - self.__popup_res[0]/2, self.screenSize[1]/2 - self.__popup_res[1]/2), self.__popup_res, self.success)
            self.selectionIndex = -1
        #continue button
        elif self.selectionIndex == 1:
            self.done = True
            self.selectionIndex = -1
            
            
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.right / 2 - self.fontSurf.get_rect().width / 2.0, self.rect.bottom / 2), self.fontSurf.get_rect())
        screen.blit(self.scoreSurf, (self.rect.right / 2 - self.scoreSurf.get_rect().width / 2.0, (self.rect.bottom / 2) + self.fontSurf.get_rect().height), self.scoreSurf.get_rect())
        for b in self.buttons:
            b.draw(screen)
            
        if self.scorePopup:
            self.scorePopup.draw(screen)
        
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
                    if not self.scorePopup:
                        for b in self.buttons:
                                if(b.click_check(event.pos)):
                                    self.selectionIndex = b.getID()
                    else:
                        if self.scorePopup.click_check(event.pos):
                            run = False
                        
        return run
        
    def get_game(self):
        return self.game