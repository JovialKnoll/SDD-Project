import pygame
import random
from miniGame import MiniGame
from Invader import *

class InvadersGame(MiniGame):
    def __init__(self, screenSize, material):
        MiniGame.__init__(self, screenSize, material)
        self.questions = [self.make_question(i) for i in range(len(self.materialCopy))]
        self.questionNum = 0
        random.shuffle(self.questions)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.defender = Defender(self.font, self.screenSize)
        self.score = 0
        self.pointsMultiplier = 255
        
    def make_question(self, x):
        question = (self.materialCopy[x][0], [], x) #term, 4 possible definitions in a random order, the index of the term in material
        if len(self.materialCopy[x][1]) < 4:
            question[1].extend(self.materialCopy[x][1])
            while len(question[1]) < 4:
                y = random.randint(0, len(self.materialCopy)-1)
                z = random.randint(0, len(self.materialCopy[y][1])-1)
                if question[1].count(self.materialCopy[y][1][z]) == 0:
                    question[1].append(self.materialCopy[y][1][z])
        else:
            question[1].append(self.materialCopy[x][1][0])
            while len(question[1]) < 4:
                z = random.randint(0, len(self.materialCopy[x][1])-1)
                if question[1].count(self.materialCopy[x][1][z]) == 0:
                    question[1].append(self.materialCopy[x][1][z])
        random.shuffle(question[1])
        return question
    
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            self.defender.process_event(event)
        if self.defender.is_complete() and self.questionNum >= len(self.questions):
            run = False
        return run
    
    def update(self):
        checkDefender = self.defender.update()
        if checkDefender != 0:
            multiplier = self.pointsMultiplier
            if checkDefender < 0:
                multiplier = 0
            self.score += ((self.pointsMultiplier + 127) * checkDefender)/25
        if self.defender.is_complete():
            if self.questionNum >= len(self.questions):
                return
            self.defender.set_question(self.questions[self.questionNum], self.materialCopy[self.questions[self.questionNum][2]][1][0])
            self.questionNum += 1
            self.pointsMultiplier = 255
        else:
            if self.pointsMultiplier > 1:
                self.pointsMultiplier -= 1
    
    def draw(self, screen):
        screen.blit(self.font.render(str(self.score), True, (0, 255, 0)), (5,5))
        self.defender.draw(screen)
    
    def get_score(self):
        return self.score

def getMaterial():
    return [("apple", ["une pomme", "un apple"]), ("banana", ["une banane", "un ananas"]), ("potato", ["une pomme de terre"]), ("grapefruit", ["un pamplemousse"]), ("orange", ["une orange"]), ("pineapple", ["un ananas", "une anana", "un pinapple", "une pomme de terre", "un apple"])]