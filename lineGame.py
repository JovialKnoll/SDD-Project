
import pygame
from random import shuffle
from random import randint
from miniGame import MiniGame
from textWrapper import get_font_surf

#Global Variables
QABORDER = 8

class QA(object):
    def __init__(self, screenSize, question, answer, posQ=(0,0), posA=(0,0)):
        f = pygame.font.SysFont(pygame.font.get_default_font(),20)
        self.imageQ = get_font_surf(f,question,screenSize[0]/2-QABORDER*2,True,(0,0,255),(0,0,0,0))
        self.imageA = get_font_surf(f,answer,screenSize[0]/2-QABORDER*2,True,(0,0,255),(0,0,0,0))
        
        self.rectQ = pygame.Rect(posQ[0]-QABORDER,posQ[1]-QABORDER,self.imageQ.get_width()+QABORDER*2,self.imageQ.get_height()+QABORDER*2)
        self.rectA = pygame.Rect(posA[0]-QABORDER,posA[1]-QABORDER,self.imageA.get_width()+QABORDER*2,self.imageA.get_height()+QABORDER*2)
        self.done = False
        
    def checkCorrect(self, pos1, pos2):
        if (self.rectQ.collidepoint(pos1) and self.rectA.collidepoint(pos2)) or (self.rectQ.collidepoint(pos2) and self.rectA.collidepoint(pos1)):
            self.done = True
            return True
        return False
    
    def touch(self, pos):
        if (self.rectQ.collidepoint(pos) or self.rectA.collidepoint(pos)):
            return True
        return False
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill((0,0,64+128*self.done), self.rectQ)
        screen.fill((0,0,64+128*self.done), self.rectA)
        screen.blit(self.imageQ, (self.rectQ[0]+QABORDER, self.rectQ[1]+QABORDER))
        screen.blit(self.imageA, (self.rectA[0]+QABORDER, self.rectA[1]+QABORDER))

class Line(object):
    def __init__(self, startPos, listQA):
        """StartPos should be a tuple of x and y position."""
        self.startPos = startPos
        self.endPos = startPos
        self.done = False
        self.correct = False
        self.count = 60
        self.listQA = listQA
        
    def checkCorrect(self):
        for qa in self.listQA:
            if qa.done:
                continue
            if qa.checkCorrect(self.startPos, self.endPos):
                self.correct = True
                return 15
        for qa1 in self.listQA:
            if qa1.touch(self.startPos):
                for qa2 in self.listQA:
                    if qa2.touch(self.endPos) and qa2 != qa1:
                        return -5
        return 0
        
    def update(self):
        if not self.done:
            self.endPos = pygame.mouse.get_pos()
            #return result of a check for correct line drawn or not
            #return 0 if not done, 1 if done correct, 2 if done incorrect
            return 0
        else:
            if self.correct:
                return 1
            else:
                self.count -= 1
                if self.count < 0:
                    return 3
                return 2
            
    def draw(self, screen):
        if (self.count/5)%2 == 0:
            pygame.draw.line(screen, (255 * (1-(self.done == self.correct)), 255 * (1-self.done), 255 * (1-self.done)), self.startPos, self.endPos)
            
class LineGame(MiniGame):
    def __init__(self, screenSize, material):
        MiniGame.__init__(self, screenSize, material)
        self.score = 0
        self.linesWrong = []
        self.currentLine = False
        self.mousePressed = False
        positionQ = [(QABORDER+(num%2)*self.screenSize[0]/2,64*(num/2)+16) for num in range(len(self.material))]
        positionA = [(QABORDER+(num%2)*self.screenSize[0]/2,screenSize[1]/2+64*(num/2)+16) for num in range(len(self.material))]
        shuffle(positionQ)
        shuffle(positionA)
        self.qas = [QA(self.screenSize,self.material[i][0],self.material[i][1][0],positionQ[i],positionA[i]) for i in range(len(self.material))]
        self.run = True
        #make list of QA's, pass to lines
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.mousePressed:
                    self.currentLine = Line(pygame.mouse.get_pos(),self.qas)
                    self.mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousePressed:
                    self.currentLine.done = True
                    self.score += self.currentLine.checkCorrect()
                    self.mousePressed = False
        return self.run
                    
    def update(self):
        MiniGame.update(self)
        self.linesWrong = [l for l in self.linesWrong if l.update() != 3]
                
        if not (self.currentLine == False):
            temp = self.currentLine.update()
            if temp == 1:
                self.objects.append(self.currentLine)
                self.currentLine = False
            elif temp == 2:
                self.linesWrong.append(self.currentLine)
                self.currentLine = False
        pygame.display.set_caption("Score: " + str(self.score))
        self.run = False
        for qa in self.qas:
            if qa.done == False:
                self.run = True
                
    def draw(self, screen):
        pygame.draw.rect(screen, (160,160,160), (0,0,screen.get_width(),screen.get_height()))
        MiniGame.draw(self, screen)
        for qa in  self.qas:
            qa.draw(screen)
        for l in self.linesWrong:
            l.draw(screen)
        if not (self.currentLine == False):
            self.currentLine.draw(screen)
    
    def get_score(self):
        return self.score
        
    def get_game(self):
        return "lineGame"