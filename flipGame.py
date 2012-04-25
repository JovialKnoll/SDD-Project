
import pygame
import random
from miniGame import MiniGame
from math import floor
from textWrapper import wrap_text
from textWrapper import get_font_surf

class Card(object):
    def __init__(self, position):
        self.term = "Hooplah"
        self.rect = pygame.Rect(position, (100,100))
        self.indexNum = -1
        self.show = False
        self.hide = False
        self.hideWhenDone = False
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
                self.update_hide()
                self.matchReset.update_hide()
                self.matchReset.matchReset = None
                self.matchReset = None
    
    def draw(self, screen, cardSurface):
        if not self.hide or self.flipping > 0:
            area = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            screen.blit(cardSurface, self.rect, area)
            if self.show:
                screen.blit(self.fontSurf, (self.rect.x, self.rect.y + (self.rect.height - self.fontSurf.get_height())/2), area)
    
    def flip(self):
        if self.flipping != 0 or self.hide:
            return False
        self.flipping = 1
        return not self.show or self.hide
    
    def reset(self, otherCard):
        self.matchReset = otherCard
    
    def reset_and_hide(self, otherCard, hide):
        self.matchReset = otherCard
        self.hideWhenDone = hide
    
    def hide(self, hide):
        self.hide = hide
        self.hideWhenDone = hide
    
    def update_hide(self):
        self.hide = self.hideWhenDone
        
class FlipGame(MiniGame):
    def __init__(self, screenSize, material):
        MiniGame.__init__(self, screenSize, material)
        self.cardSurface = pygame.Surface((100, 100))
        self.cardSurface.fill((75, 200, 75))
        if not material:
            self.material = [("Spongebob", ["Squarepants"]), ("Patrick", ["Star"]), ("Squidward", ["Tentacles"])]
        else:
            self.material = material
        self.cards = [Card(((i%5)*150, floor(i/5) * 150 + 150)) for i in range(0, len(self.material) * 2)]
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.itemsFlipped = []
        self.score = 0
        random.shuffle(self.cards)
        for i in range(len(self.cards)):
            if i%2 == 0:
                self.cards[i].term = self.material[i/2][0]
                self.cards[i].fontSurf = get_font_surf(self.font, self.cards[i].term, 100, True, (0,0,0), (75,200,75))
                self.cards[i].indexNum = i/2
            else:
                self.cards[i].term = self.material[int(floor(i/2))][1][0]
                self.cards[i].fontSurf = get_font_surf(self.font, self.cards[i].term, 100, True, (0,0,0), (75,200,75))
        
    
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
                        self.flip_card(card)
        return run
    
    def update(self):
        for card in self.cards:
            card.update()
        pygame.display.set_caption("Score: " + str(self.score))
    
    def draw(self, screen):
        for card in self.cards:
            card.draw(screen, self.cardSurface)
        #scoresurf = self.font.render("Score: " + str(self.score) + " points", True, (50,250,50))
        #screen.blit(scoresurf, (50, 50), scoresurf.get_rect())
    
    def flip_card(self, card):
        if card.flip():
            self.itemsFlipped.append(card)
            if len(self.itemsFlipped) > 1:
                match = False
                if self.itemsFlipped[0].indexNum > -1:
                    if self.material[self.itemsFlipped[0].indexNum][1][0] == card.term:
                        self.score += 10
                        match = True
                        print self.score
                    
                if card.indexNum > -1:
                    if self.itemsFlipped[0].term == self.material[card.indexNum][1][0]:
                        self.score += 10
                        match = True
                        print self.score
                self.itemsFlipped[0].reset_and_hide(card, match)
                card.reset_and_hide(self.itemsFlipped[0], match)
                self.itemsFlipped = []
        elif len(self.itemsFlipped) > 0 and self.itemsFlipped[0] == card:
            self.itemsFlipped.remove(card)
    
    def get_score(self):
        return self.score