
import pygame
import random
from miniGame import MiniGame
from math import floor

class Card(object):
    def __init__(self, position):
        self.term = "Hooplah"
        self.rect = pygame.Rect(position, (100,100))
        self.indexNum = -1
        self.show = False
        self.flipping = False
        self.matchReset = None
        
    def update(self):
        if self.flipping == 2:
            newWidth = max(5, self.rect.width * 2)
            if newWidth > 100:
                self.flipping = 0
                newWidth = 100
            self.rect.width = newWidth
        if self.flipping == 1:
            newWidth = self.rect.width * 2 - 105
            if newWidth < 0:
                self.flipping = 2
                self.show = not self.show
                newWidth = 1
            self.rect.width = newWidth
        if self.matchReset != None and self.flipping == 0:
            if self.matchReset.flipping == 0:
                self.flip()
                self.matchReset.flip()
                self.matchReset.matchReset = None
                self.matchReset = None
    
    def draw(self, screen, cardSurface):
        area = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        screen.blit(cardSurface, self.rect, area)
        if self.show:
            screen.blit(self.fontSurf, (self.rect.x, self.rect.y + (self.rect.height - self.fontSurf.get_height())/2), area)
    
    def flip(self):
        if self.flipping != 0:
            return False
        self.flipping = 1
        return not self.show
    
    def reset(self, otherCard):
        self.matchReset = otherCard
        
class FlipGame(MiniGame):
    def __init__(self, material):
        MiniGame.__init__(self, material)
        self.cardSurface = pygame.Surface((100, 100))
        self.cardSurface.fill((75, 200, 75))
        self.material = [("Spongebob", ["Squarepants"]), ("Patrick", ["Star"]), ("Squidward", ["Tentacles"])]
        self.cards = [Card(((i%5)*150, floor(i/5) * 150 + 150)) for i in range(0, len(self.material) * 2)]
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.itemsFlipped = []
        self.score = 0
        random.shuffle(self.cards)
        for i in range(len(self.cards)):
            if i%2 == 0:
                self.cards[i].term = self.material[i/2][0]
                self.cards[i].fontSurf = self.font.render(self.cards[i].term, True, (0,0,0))
                self.cards[i].indexNum = i/2
            else:
                self.cards[i].term = self.material[int(floor(i/2))][1][0]
                self.cards[i].fontSurf = self.font.render(self.cards[i].term, True, (0,0,0))
        
        
    
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = event.pos
                for card in self.cards:
                    if card.rect.collidepoint(mousePos):
                        if card.flip():
                            self.itemsFlipped.append(card)
                            if len(self.itemsFlipped) > 1:
                                match = False
                                if self.itemsFlipped[0].indexNum > -1:
                                    if self.material[self.itemsFlipped[0].indexNum][1][0] == card.term:
                                        self.score += 10
                                        print self.score
                                        
                                if card.indexNum > -1:
                                    if self.itemsFlipped[0].term == self.material[card.indexNum][1][0]:
                                        self.score += 10
                                        print self.score
                                self.itemsFlipped[0].reset(card)
                                card.reset(self.itemsFlipped[0])
                                self.itemsFlipped = []
                        else:
                            self.itemsFlipped.remove(card)
        return run
    
    def update(self):
        for card in self.cards:
            card.update()
    
    def draw(self, screen):
        for card in self.cards:
            card.draw(screen, self.cardSurface)
        scoresurf = self.font.render("Score: " + str(self.score) + " points", True, (50,250,50))
        screen.blit(scoresurf, (50, 50), scoresurf.get_rect())