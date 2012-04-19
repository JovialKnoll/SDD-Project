
import pygame
from random import shuffle
from miniGame import MiniGame

class QA(object):
    def __init__(self, question, answer, posQ=(0,0), posA=(0,0)):
        
        #self.question = question
        #self.answer = answer
        f = pygame.font.SysFont(pygame.font.get_default_font(),20)
        #print question
        #print answer
        self.qSize = f.size(question)
        self.aSize = f.size(answer)
        self.qImage = f.render(question,False,(0,0,255))
        self.aImage = f.render(answer,False,(0,0,255))
        self.rectQ = pygame.Rect(posQ[0],posQ[1],self.qSize[0],self.qSize[1])
        self.rectA = pygame.Rect(posA[0],posA[1],self.aSize[0],self.aSize[1])
        self.done = False
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.qImage, (self.rectQ[0], self.rectQ[1]))
        screen.blit(self.aImage, (self.rectA[0], self.rectA[1]))

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
            if (qa.rectQ.collidepoint(self.startPos) and qa.rectA.collidepoint(self.endPos)) or (qa.rectQ.collidepoint(self.endPos) and qa.rectA.collidepoint(self.startPos)):
                self.correct = True
                qa.done = True
                break
        
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
        self.linesWrong = []
        self.currentLine = False
        self.mousePressed = False
        horizontalPositionsQ = [(i*self.screenSize[0]/len(self.material)) for i in range(len(self.material))]
        horizontalPositionsA = [(i*self.screenSize[0]/len(self.material)) for i in range(len(self.material))]
        shuffle(horizontalPositionsQ)
        shuffle(horizontalPositionsA)
        self.qas = [QA(self.material[num][0],self.material[num][1],(horizontalPositionsQ[num],screenSize[0]/3),(horizontalPositionsA[num],screenSize[0]*2/3)) for num in range(len(self.material))]
        
        #make list of QA's, pass to lines
        
    def process_events(self):
        run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.mousePressed:
                    self.currentLine = Line(pygame.mouse.get_pos(),self.qas)
                    self.mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousePressed:
                    self.currentLine.done = True
                    self.currentLine.checkCorrect()
                    self.mousePressed = False
        return run
                    
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
                
    def draw(self, screen):
        pygame.draw.rect(screen, (160,160,160), (0,0,screen.get_width(),screen.get_height()))
        MiniGame.draw(self, screen)
        for qa in  self.qas:
            qa.draw(screen)
        for l in self.linesWrong:
            l.draw(screen)
        if not (self.currentLine == False):
            self.currentLine.draw(screen)