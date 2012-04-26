#
# Invader.py is a collection of helper classes for InvadersGame
#
import pygame
from textWrapper import wrap_text
from textWrapper import get_font_surf
from math import copysign as sign

class Sprite(object):
    """ A useful class for moving images around the screen"""
    def __init__(self, image, position):
        """ Create a Sprite with a given image and starting position """
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], image.get_width(), image.get_height())
    
    def draw(self, screen):
        """ draw the Sprite to screen """
        screen.blit(self.image, self.rect)
    
    def move(self, x, y):
        self.rect.move_ip(x, y)
    
    def collide_rect(self, rect):
        """ returns whether or not rect is colliding with this Sprite """
        return self.rect.colliderect(rect)
    
    def collide_sprite(self, sprite):
        """ returns whether or not the given Sprite is colliding with this Sprite """
        return sprite.collide_rect(self.rect)
    
    def past_edge(self, width):
        """ checks if the sprite is horizontally out of the bounds [0, width] """
        return self.rect.x < 0 or self.rect.x + self.rect.width > width

class Bullet(Sprite):
    """ a class that models the behavior of the bullet that the defender shoots """
    def __init__(self, image, position):
        Sprite.__init__(self, image, position)
        self.speed = 25 #the speed at which the bullet travels
        self.moveDir = -1 #the vertical direction the bullet travels
        self.homing = False #whether or not the bullet seeks a target
        self.father = self.rect #the target that the bullet seeks
    
    def set_father(self, father):
        """ set the father, or target for the bullet to seek """
        self.father = father
    
    def return_to_sender(self):
        """ bounce the bullet back at the father """
        self.homing = True
        self.moveDir *= -1
    
    def is_homing(self):
        return self.homing
    
    def update(self):
        """ move the bullet forward, return its position for collision and bound checking """
        xMove = 0
        if self.homing and self.father != None:
            xMove = sign(self.speed/5, self.father.centerx - self.rect.centerx)
        self.move(xMove, self.speed * self.moveDir)
        return self.rect.y
        
class Invader(object):
    """ a class that represents a set of possible responses for an answer, represented a 4 spaceships """
    def __init__(self, answers, correctAnswer, font, screenSize):
        """ create an invader with the given answers """
        self.answers = answers #the text of all possible answers
        self.correctAnswer = correctAnswer #the text of the correct answer
        self.font = font #the font used for rendering the text
        self.screenSize = screenSize #the size of the display screen, used for scaling objects
        self.sprites = self.make_sprites() #the sprites of the answers
        self.moveDir = 1 #which direction the sprites are strafing
    
    def make_sprites(self):
        """ create the list of sprites for the invader, scaled by the screen size """
        self.unitWidth = self.screenSize[0] / 7;
        self.unitHeight = self.unitWidth
        return [self.make_sprite(self.answers[i], (i * self.unitWidth * 5/3 + self.unitWidth/2, 30)) for i in range(len(self.answers))]
    
    def make_sprite(self, text, position):
        """ create a single invader sprite, with given text and starting position """
        #create the background image
        image = pygame.Surface((self.unitWidth, self.unitHeight))
        image.fill((250, 150, 150))
        #add the text to the image
        textImage = get_font_surf(self.font, text,image.get_width(), True, (0,0,0), (250,150,150))
        image.blit(textImage, ((self.unitWidth-textImage.get_width())/2, (self.unitHeight-textImage.get_height())/2))
        #create the sprite
        spr = Sprite(image, position)
        return spr
    
    def move(self, dist):
        """ move all of the sprites dist pixels in the movement direction """
        for i in self.sprites:
            i.move(dist*self.moveDir, 0)
        if self.sprites[0].past_edge(self.screenSize[0]) or self.sprites[len(self.sprites)-1].past_edge(self.screenSize[0]):
            #if the sprites have reached an edge, change direction
            self.moveDir *= -1
    
    def bullet_check(self, bullet):
        """ check if a bullet is colliding with an answer, bounce the bullet back if it is hitting an incorrect answer, return 1 if hit correct answer """
        for i in range(len(self.sprites)):
            if self.sprites[i].collide_sprite(bullet):
                print "Hit " + self.answers[i] + ", correct answer was " + self.correctAnswer
                if self.answers[i] == self.correctAnswer:
                    return 1
                else:
                    bullet.return_to_sender()
        return 0
    
    def draw(self, screen):
        """ draw to screen """
        for i in self.sprites:
            i.draw(screen)

class Defender(object):
    """ The player-controlled piece that shoots at the invaders and displays the term/question """
    def __init__(self, font, screenSize):
        """ create a new defender, by default does not have a question """
        self.text = "" #the term
        self.answer = "" #the correct response to the term
        self.font = font #the font for rendering all text
        self.screenSize = screenSize #the size of the display, for scaling
        self.width = screenSize[0] / 4 #width of the defender
        self.height = self.width * 2 / 3 #height of the defender
        
        #create the defender's image
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(0, self.height/5, self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(self.width/2 - self.height/10, 0, self.height/5, self.height/5))
        self.rect = pygame.Rect((screenSize[0] - self.width)/2, screenSize[1] - self.height, self.width, self.height) #size and position for display and collision
        self.refresh_text_surface() #the text displayed on the defender
        
        self.invaders = None #by default, no invaders, is set in set_question
        self.bullet = None #the bullet that the defender has shot, can only have one bullet on screen at a time
        self.bulletSurf = pygame.Surface((25, 25)) #the image used to create all bullet sprites
        self.bulletSurf.fill((255,0,0))
        self.speed = 17 #defender's movement speed
        self.moving = [0, 0] #left and right keys used for determining move direction
    
    def set_question(self, question, answer):
        """ set the question being asked, create new invaders """
        self.text = question[0]
        self.answer = answer
        self.refresh_text_surface()
        self.invaders = Invader(question[1], self.answer, self.font, self.screenSize)
    
    def refresh_text_surface(self):
        """ using the current text, set the image for the text """
        #get_font_surf creates a surface with the text wrapped to a certain width
        self.textSurface = get_font_surf(self.font, self.text,self.image.get_width(), True, (0,0,0), (150,150,250))
        self.textRect = pygame.Rect((self.width - self.textSurface.get_width())/2, (self.height - self.textSurface.get_height())/2, 0, 0)
    
    def bullet_check(self, bullet):
        """ check if the bullet has his the defender. Returns -1 if it has, 0 if it hasn't """
        if bullet.collide_rect(self.rect):
            return -1
        return 0
    
    def process_event(self, event):
        """ takes an event and updates the defender based on it """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #start moving left
                self.moving[0] = -1
            elif event.key == pygame.K_RIGHT:
                #start moving right
                self.moving[1] = 1
            elif event.key == pygame.K_SPACE and self.bullet == None:
                #shoot a bullet
                self.bullet = Bullet(self.bulletSurf, (self.rect.centerx - self.bulletSurf.get_width()/2, self.rect.top + self.bulletSurf.get_height()))
                self.bullet.set_father(self.rect)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                #stop moving left
                self.moving[0] = 0
            elif event.key == pygame.K_RIGHT:
                #stop moving right
                self.moving[1] = 0
    
    def update(self):
        """ update self, invaders, bullet, and return the sign of the score change to make """
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
        """ whether or not the player has completed the current question """
        return self.invaders == None
    
    def draw(self, screen):
        """ draw everything to the screen """
        screen.blit(self.image, self.rect)
        screen.blit(self.textSurface, (self.textRect.x + self.rect.x, self.textRect.y + self.rect.y))
        if self.invaders != None:
            self.invaders.draw(screen)
        if self.bullet != None:
            self.bullet.draw(screen)