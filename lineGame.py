
import pygame
from random import shuffle
from miniGame import MiniGame

class QA(object):
    def __init__(self, question, answer, posQ=0, posA=0):
        
        #self.question = question
        #self.answer = answer
        self.qSize = Font.size(question)
        self.aSize = Font.size(answer)
        self.qImage = pygame.font.SysFont(pygame.font.get_default_font(),12).render(question,False,(0,0,255))
        self.aImage = pygame.font.SysFont(pygame.font.get_default_font(),12).render(answer,False,(0,0,255))
        self.posQ = posQ
        self.posA = posA
        self.done = False
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.qImage, (self.posQ, screen.get_height()/3))
        screen.blit(self.aImage, (self.posA, screen.get_height()*2/3))

class Line(object):
    def __init__(self, startPos, listQA):
        """StartPos should be a tuple of x and y position."""
        self.startPos = startPos
        self.endPos = startPos
        self.done = False
        self.correct = True
        self.count = 60
        self.listQA = listQA
        
    def isCorrect(self):
        pass
        
    def update(self):
        if not self.done:
            self.endPos = pygame.mouse.get_pos()
            #return result of a check for correct line drawn or not
            #return 0 if not done, 1 if done correct, 2 if done incorrect
            return 0
        else:
            t = False#replace with actually finding if correct or not
            if t:
                return 1
            else:
                self.correct = False
                self.count -= 1
                if self.count < 0:
                    return 3
                return 2
            
    def draw(self, screen):
        if (self.count/5)%2 == 0:
            pygame.draw.line(screen, (255 * (1-self.correct), 255 * (1-self.done), 255 * (1-self.done)), self.startPos, self.endPos)
            
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
        self.qas = [QA(self.material[num],horizontalPositionsQ[num],horizontalPositionsA[num]) for num in range(len(self.material))]
        
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
        for l in self.linesWrong:
            l.draw(screen)
        if not (self.currentLine == False):
            self.currentLine.draw(screen)