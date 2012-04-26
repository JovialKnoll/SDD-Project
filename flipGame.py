#
# flipGame.py is a miniGame that does memory card-matching
#
import pygame
import random
from miniGame import MiniGame
from math import floor
from textWrapper import wrap_text
from textWrapper import get_font_surf

class Card(object):
    """ the object that represents a card """
    def __init__(self, position):
        """ create a card at a given position """
        self.term = "Hooplah" #the text written on the card
        self.rect = pygame.Rect(position, (100,100)) #the size and position of the card
        self.indexNum = -1 #-1 if card is a definition, the index of the term in the material if card is a term
        self.show = False #True if the card is face-up, False if it is face-down
        self.hide = False #True if this card is invisible (removed from the table)
        self.hideWhenDone = False #when the card is done flipping, will it be hidden?
        self.flipping = False #how the card is currently in the process of flipping (0=not, 1=shrinking, 2=growing)
        self.matchReset = None #the card this card is matched with, they flip back in unison
        
    def update(self):
        """ animates flipping and auto-resets when a match is made """
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
            # if this card is matched with another
            if self.matchReset.flipping == 0:
                #wait until both cards are finished flipping, and then reset them both
                self.flip()
                self.matchReset.flip()
                self.update_hide()
                self.matchReset.update_hide()
                self.matchReset.matchReset = None
                self.matchReset = None
    
    def draw(self, screen, cardSurface):
        """ draw the card, and if the text is showing, draw the text """
        if not self.hide or self.flipping > 0:
            area = pygame.Rect(0, 0, self.rect.width, self.rect.height)
            screen.blit(cardSurface, self.rect, area)
            if self.show:
                screen.blit(self.fontSurf, (self.rect.x, self.rect.y + (self.rect.height - self.fontSurf.get_height())/2), area)
    
    def flip(self):
        """ flip the card, return true if you are revealing this card """
        if self.flipping != 0 or self.hide:
            return False
        self.flipping = 1
        return not self.show or self.hide
    
    def reset(self, otherCard):
        """ match this card with otherCard """
        self.matchReset = otherCard
    
    def reset_and_hide(self, otherCard, hide):
        """ match this card with otherCard and remove it from the table after it has reset if hide is true"""
        self.matchReset = otherCard
        self.hideWhenDone = hide
    
    def hide(self, hide):
        """ remove this card from the table """
        self.hide = hide
        self.hideWhenDone = hide
    
    def update_hide(self):
        """ remove this card from the table only if it is scheduled to be removed """
        self.hide = self.hideWhenDone
    
    def finished(self):
        """ returns whether or not this card has been removed from the table """
        return self.hide and not self.flipping > 0
        
class FlipGame(MiniGame):
    """ a memory-flip mini-game """
    def __init__(self, screenSize, material):
        MiniGame.__init__(self, screenSize, material)
        self.cardSurface = pygame.Surface((100, 100)) #the image all cards use
        self.cardSurface.fill((75, 200, 75))
        self.rowWidth = screenSize[0] / 150 #the number of rows wide the screen is
        self.rowHeight = (screenSize[1] - 15)/ 150 #the number of rows tall the screen is
        maxLength = ((self.rowWidth * self.rowHeight) / 2)  #max number of card pairs displayed on one screen
        if not material:
            self.material = [("Spongebob", ["Squarepants"]), ("Patrick", ["Star"]), ("Squidward", ["Tentacles"])]
        else:
            self.material = material
        
        #create a table of cards
        self.cards = [Card(((i%self.rowWidth)*150, floor(i/5) * 150 + 15)) for i in range(0, min(len(self.material), maxLength) * 2)]
        
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12) #font for rendering all text
        self.itemsFlipped = [] #list of cards that have been flipped
        self.score = 0 #player's score
        self.scoreMultiplier = len(self.cards) * 100 #multiplier for player's score based on speed
        
        #shuffle and set the text for all cards
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
        """ handle input """
        run = False
        for card in self.cards: # check if the table has been cleared
            if not card.finished():
                run = True
                break
        else:
            print self.scoreMultiplier
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
                        #if you click on a card, flip it
                        self.flip_card(card)
        return run
    
    def update(self):
        """ run one game step """
        #update all the cards
        for card in self.cards:
            card.update()
        #update the score multiplier
        if self.scoreMultiplier > 1:
            self.scoreMultiplier -= 1
        pygame.display.set_caption("Score: " + str(self.score * (self.scoreMultiplier + len(self.cards)*100)/(len(self.cards)*50)))
    
    def draw(self, screen):
        """ draw all the cards """
        for card in self.cards:
            card.draw(screen, self.cardSurface)
        #scoresurf = self.font.render("Score: " + str(self.score) + " points", True, (50,250,50))
        #screen.blit(scoresurf, (50, 50), scoresurf.get_rect())
    
    def flip_card(self, card):
        """ flip a card """
        if card.flip():
            self.itemsFlipped.append(card) #add it to the list of flipped cards
            if len(self.itemsFlipped) > 1: #if you have flipped 2 cards
                match = False
                #check if they match
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
                #flip both cards back over
                self.itemsFlipped[0].reset_and_hide(card, match)
                card.reset_and_hide(self.itemsFlipped[0], match)
                self.itemsFlipped = []
        elif len(self.itemsFlipped) > 0 and self.itemsFlipped[0] == card:
            self.itemsFlipped.remove(card) #if you flip one back over, remove it from the list of flipped cards
    
    def get_score(self):
        """ return the player's score """
        return (self.score * (self.scoreMultiplier + len(self.cards)*100)/(len(self.cards)*50))

    def get_game(self):
        return "flipGame"

