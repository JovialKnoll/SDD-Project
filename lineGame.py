
import pygame
from miniGame import MiniGame

class Line(object):
    def __init__(self, startPos):
        """StartPos should be a tuple of x and y position."""
        self.startPos = startPos
        self.endPos = startPos
        self.done = False
        self.correct = True
        
    def update(self):
        if not self.done:
            self.endPos = pygame.mouse.get_pos()
            #return result of a check for correct line drawn or not
            #return 0 if not done, 1 if done correct, 2 if done incorrect
            return 0
        else:
            return 1
            
    def draw(self, screen):
        pygame.draw.line(screen, (255 * (1-self.correct), 255 * (1-self.done), 0), self.startPos, self.endPos)

class LineGame(MiniGame):
    def __init__(self, material):
        MiniGame.__init__(self, material)
        self.linesWrong = []
        self.currentLine = False
        self.mousePressed = False
        
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
                    self.currentLine = Line(pygame.mouse.get_pos())
                    self.mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousePressed:
                    self.currentLine.done = True
                    self.mousePressed = False
                
        return run
                    
    def update(self):
        MiniGame.update(self)
        for l in self.linesWrong:
            l.update()
        if not (self.currentLine == False):
            temp = self.currentLine.update()
            if temp == 1:
                self.objects.append(self.currentLine)
                self.currentLine = False
            elif temp == 2:
                self.linesWrong.append(self.currentLine)
                self.currentLine = False
                
    def draw(self, screen):
        pygame.draw.rect(screen, (200,200,200), (0,0,screen.get_width(),screen.get_height()))
        MiniGame.draw(self, screen)
        for l in self.linesWrong:
            l.draw(screen)
        if not (self.currentLine == False):
            self.currentLine.draw(screen)