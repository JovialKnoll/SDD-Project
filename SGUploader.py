import pygame
from gbxml import upload
from gbxml import listLocalXMLFiles

class LineItem(object):
    
    
    def __init__(self, pos, text, res, id):
        """One study guide line item"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 20)
        temp = text.replace("xml/", "")
        self.fontSurf = self.font.render(temp, False, (0,0,0))
        self.sprite = pygame.image.load("gfx/lineItem.png").convert_alpha()
        self.id = id
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left, self.rect.top), self.fontSurf.get_rect())
        
    def clickCheck(self, pos):
        return self.rect.collidepoint(pos)
        
    def getID(self):
        return self.id
     
     
class LoaderPopup(object):
    
    def __init__(self, pos, res, loaded):
        """Defines the success/fail of the operation"""
        self.rect = pygame.Rect(pos, res)
        self.font = pygame.font.SysFont("Courier", 16)
        if loaded:
            self.fontSurf = self.font.render("Guide uploaded successfully.", False, (0,0,0))
        else:
            self.fontSurf = self.font.render("Failed upload of selected file.", False, (0,0,0))
        self.sprite = pygame.image.load("gfx/loaderPopup.png").convert_alpha()
        
    def draw(self,screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        screen.blit(self.fontSurf, (self.rect.left + self.rect.width/2.0 - self.fontSurf.get_rect().width/2.0, self.rect.top + self.rect.height/2.0 - self.fontSurf.get_rect().height/2.0),
        self.fontSurf.get_rect())
        
    def clickCheck(self, pos):
        return self.rect.collidepoint(pos)


        
class SGUploader(object):
    
    __res = (600, 400)
    __lineItemOffset = 20
    __separationLine = 5
    __popup_res = (300, 200)
    
    def __init__(self, screenSize):
        """Downloads guides from the server to the local client"""
        self.rect = pygame.Rect(((screenSize[0] - self.__res[0]) / 2, (screenSize[1] - self.__res[1]) / 2), self.__res)
        self.sprite = pygame.image.load("gfx/guideLoader.png").convert_alpha()
        self.screenSize = screenSize
        
        #get local files in the /xml folder
        self.files = listLocalXMLFiles()
        self.selectionIndex = -1
        self.success = False
        self.loadPopup = False
        
        #create line items for each file found
        self.lineItems = []
        for i in range(0, len(self.files)):
            if i == 0:
                 self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1]), self.files[i], (self.__res[0], self.__lineItemOffset), i))
            else:
                self.lineItems.append(LineItem((self.rect.topleft[0], self.rect.topleft[1] +  self.__lineItemOffset * i + self.__separationLine * i),
                self.files[i], (self.__res[0], self.__lineItemOffset), i))
                
    def update(self):
        #upload file based on selected line item
        if self.selectionIndex > -1:
            temp = self.files[self.selectionIndex]
            temp = temp.replace("xml/", "")
            self.success = upload(temp)    
            self.selectionIndex = -1
            self.loadPopup = LoaderPopup((self.screenSize[0]/2 - self.__popup_res[0]/2, self.screenSize[1]/2 - self.__popup_res[1]/2), self.__popup_res, self.success)
    
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.left, self.rect.top), self.sprite.get_rect())
        for l in self.lineItems:
            l.draw(screen)
        if self.loadPopup:
            self.loadPopup.draw(screen)
        
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if not self.loadPopup:
                    for l in self.lineItems:
                        if(l.clickCheck(event.pos)):
                            self.selectionIndex = l.getID()
                else:
                    if(self.loadPopup.clickCheck(event.pos)):
                        run = False
                        
        return run