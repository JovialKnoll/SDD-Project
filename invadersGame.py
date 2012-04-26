#
# InvadersGame.py is a MiniGame in the style of space invaders
#
import pygame
import random
from miniGame import MiniGame
from Invader import *

class InvadersGame(MiniGame):
    """ a subclass of MiniGame that plays the space invaders mini-game """
    def __init__(self, screenSize, material):
        MiniGame.__init__(self, screenSize, material)
        self.questions = [self.make_question(i) for i in range(len(self.materialCopy))] #convert the material into a form the game can use
        self.questionNum = 0 #the index of the current question
        random.shuffle(self.questions) #randomize the order in which the questions appear
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12) #the font with which to render all text
        self.defender = Defender(self.font, self.screenSize) #the player-controlled defender, see Invader.py
        self.score = 0 #the player's score
        self.pointsMultiplier = 255 #a score modifier that decreases over time
        
    def make_question(self, x):
        """ turn an element from the material into a question that the Defender and Invader class can read """
        question = (self.materialCopy[x][0], [], x) #term, 4 possible definitions in a random order, the index of the term in material
        if len(self.materialCopy[x][1]) < 4:
            #if there are not enough decoys, choose random responses from other terms
            question[1].extend(self.materialCopy[x][1])
            while len(question[1]) < 4:
                y = random.randint(0, len(self.materialCopy)-1)
                z = random.randint(0, len(self.materialCopy[y][1])-1)
                #make sure you don't repeat any responses
                if question[1].count(self.materialCopy[y][1][z]) == 0:
                    question[1].append(self.materialCopy[y][1][z])
        else:
            #if there are enough decoys, choose randomly from these decoys
            question[1].append(self.materialCopy[x][1][0])
            while len(question[1]) < 4:
                z = random.randint(0, len(self.materialCopy[x][1])-1)
                if question[1].count(self.materialCopy[x][1][z]) == 0:
                    question[1].append(self.materialCopy[x][1][z])
        random.shuffle(question[1]) #mix up the order of the responses
        return question
    
    def process_events(self):
        """ handles all input """
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            self.defender.process_event(event) #pass on all input for the defender to process (movement, shooting)
        if self.defender.is_complete() and self.questionNum >= len(self.questions):
            run = False
        return run
    
    def update(self):
        """ run one game step """
        checkDefender = self.defender.update() #update the defender and check for score change
        if checkDefender != 0:
            #if the score has changed, update the score
            multiplier = self.pointsMultiplier #you get more points for answering quickly
            if checkDefender < 0:
                multiplier = 0
            self.score += ((self.pointsMultiplier + 127) * checkDefender)/25
        if self.defender.is_complete():
            #if the current question has completed, go to the next one
            if self.questionNum >= len(self.questions):
                return
            self.defender.set_question(self.questions[self.questionNum], self.materialCopy[self.questions[self.questionNum][2]][1][0])
            self.questionNum += 1
            self.pointsMultiplier = 255
        else:
            if self.pointsMultiplier > 1:
                self.pointsMultiplier -= 1 #clock is ticking!
        #show the score in the title
        pygame.display.set_caption("Score: " + str(self.score))
    
    def draw(self, screen):
        """ draw all objects """
        #screen.blit(self.font.render(str(self.score), True, (0, 255, 0)), (5,5))
        self.defender.draw(screen)
    
    def get_score(self):
        """ allows the Game to get your score """
        return self.score
        
    def get_game(self):
        return "invadersGame"

def getMaterial():
    """ get some default material, for testing """
    return [("apple", ["une pomme", "un apple"]), ("banana", ["une banane", "un ananas"]), ("potato", ["une pomme de terre"]), ("grapefruit", ["un pamplemousse"]), ("orange", ["une orange"]), ("pineapple", ["un ananas", "une anana", "un pinapple", "une pomme de terre", "un apple"])]