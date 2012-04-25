import pygame
from textWrapper import wrap_text
from textWrapper import get_font_surf
from math import copysign as sign

class Sprite(object):
    def __init__(self, image, position):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], image.get_width(), image.get_height())
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def move(self, x, y):
        self.rect.move_ip(x, y)
    
    def collide_rect(self, rect):
        return self.rect.colliderect(rect)
    
    def collide_sprite(self, sprite):
        return sprite.collide_rect(self.rect)
    
    def past_edge(self, width):
        return self.rect.x < 0 or self.rect.x + self.rect.width > width

class Bullet(Sprite):
    def __init__(self, image, position):
        Sprite.__init__(self, image, position)
        self.speed = 25
        self.moveDir = -1
        self.homing = False
        self.father = self.rect
    
    def set_father(self, father):
        self.father = father
    
    def return_to_sender(self):
        self.homing = True
        self.moveDir *= -1
    
    def is_homing(self):
        return self.homing
    
    def update(self):
        xMove = 0
        if self.homing and self.father != None:
            xMove = sign(self.speed/5, self.father.centerx - self.rect.centerx)
        self.move(xMove, self.speed * self.moveDir)
        return self.rect.y
        
class Invader(object):
    def __init__(self, answers, correctAnswer, font, screenSize):
        self.answers = answers
        self.correctAnswer = correctAnswer
        self.font = font
        self.screenSize = screenSize
        self.sprites = self.make_sprites()
        self.moveDir = 1
    
    def make_sprites(self):
        self.unitWidth = self.screenSize[0] / 7;
        self.unitHeight = self.unitWidth
        return [self.make_sprite(self.answers[i], (i * self.unitWidth * 5/3 + self.unitWidth/2, 30)) for i in range(len(self.answers))]
    
    def make_sprite(self, text, position):
        image = pygame.Surface((self.unitWidth, self.unitHeight))
        image.fill((250, 150, 150))
        textImage = get_font_surf(self.font, text,image.get_width(), True, (0,0,0), (250,150,150))
        image.blit(textImage, ((self.unitWidth-textImage.get_width())/2, (self.unitHeight-textImage.get_height())/2))
        spr = Sprite(image, position)
        return spr
    
    def move(self, dist):
        for i in self.sprites:
            i.move(dist*self.moveDir, 0)
        if self.sprites[0].past_edge(self.screenSize[0]) or self.sprites[len(self.sprites)-1].past_edge(self.screenSize[0]):
            self.moveDir *= -1
    
    def bullet_check(self, bullet):
        for i in range(len(self.sprites)):
            if self.sprites[i].collide_sprite(bullet):
                print "Hit " + self.answers[i] + ", correct answer was " + self.correctAnswer
                if self.answers[i] == self.correctAnswer:
                    return 1
                else:
                    bullet.return_to_sender()
        return 0
    
    def draw(self, screen):
        for i in self.sprites:
            i.draw(screen)

class Defender(object):
    def __init__(self, font, screenSize):
        self.text = ""
        self.answer = ""
        self.font = font
        self.screenSize = screenSize
        self.width = screenSize[0] / 4
        self.height = self.width * 2 / 3
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(0, self.height/5, self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(self.width/2 - self.height/10, 0, self.height/5, self.height/5))
        self.rect = pygame.Rect((screenSize[0] - self.width)/2, screenSize[1] - self.height, self.width, self.height)
        self.refresh_text_surface()
        self.invaders = None
        self.bullet = None
        self.bulletSurf = pygame.Surface((25, 25))
        self.bulletSurf.fill((255,0,0))
        self.speed = 17
        self.timerTicks = 0
        self.moving = [0, 0]
    
    def set_question(self, question, answer):
        self.text = question[0]
        self.answer = answer
        self.refresh_text_surface()
        self.invaders = Invader(question[1], self.answer, self.font, self.screenSize)
    
    def refresh_text_surface(self):
        self.textSurface = get_font_surf(self.font, self.text,self.image.get_width(), True, (0,0,0), (150,150,250))
        self.textRect = pygame.Rect((self.width - self.textSurface.get_width())/2, (self.height - self.textSurface.get_height())/2, 0, 0)
    
    def bullet_check(self, bullet):
        if bullet.collide_rect(self.rect):
            return -1
        return 0
    
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving[0] = -1
            elif event.key == pygame.K_RIGHT:
                self.moving[1] = 1
            elif event.key == pygame.K_SPACE and self.bullet == None:
                self.bullet = Bullet(self.bulletSurf, (self.rect.centerx - self.bulletSurf.get_width()/2, self.rect.top + self.bulletSurf.get_height()))
                self.bullet.set_father(self.rect)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving[0] = 0
            elif event.key == pygame.K_RIGHT:
                self.moving[1] = 0
    
    def update(self):
        points = 0
        if self.invaders != None:
            self.invaders.move(self.speed // 3)
            if self.bullet != None:
                bullety = self.bullet.update()
                if bullety < -25 or bullety > self.screenSize[1]:
                    self.bullet = None
                else:
                    if self.bullet.is_homing():
                        points = self.bullet_check(self.bullet)
                    else:
                        points = self.invaders.bullet_check(self.bullet)
            if points != 0:
                if points > 0:
                    self.invaders = None
                self.bullet = None
                
        move = self.moving[0] + self.moving[1]
        self.rect.move_ip(self.speed * move, 0)
        if self.rect.x + self.width > self.screenSize[0]:
            self.rect.x = self.screenSize[0] - self.width
        elif self.rect.x < 0:
            self.rect.x = 0
        return points
    
    def is_complete(self):
        return self.invaders == None
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.textSurface, (self.textRect.x + self.rect.x, self.textRect.y + self.rect.y))
        if self.invaders != None:
            self.invaders.draw(screen)
        if self.bullet != None:
            self.bullet.draw(screen)