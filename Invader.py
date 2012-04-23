import pygame

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

class Invader(object):
    def __init__(self, answers, correctAnswer, font, screenSize):
        self.answers = answers
        self.correctAnswer = correctAnswer
        self.font = font
        self.sprites = self.make_sprites()
    
    def make_sprites(self):
        return [self.make_sprite(self.answers[i], (i * 300 + 100, -100)) for i in range(len(self.answers))]
    
    def make_sprite(self, text, position):
        image = pygame.Surface((200, 150))
        image.fill((250, 150, 150))
        textImage = self.font.render(text, True, (0,0,0))
        image.blit(textImage, ((200-textImage.get_width())/2, (150-textImage.get_height())/2))
        spr = Sprite(image, position)
        return spr
    
    def move(self, dist):
        for i in self.sprites:
            i.move(0, dist)
    
    def draw(self, screen):
        for i in self.sprites:
            i.draw(screen)

class Defender(object):
    def __init__(self, font, screenSize):
        self.text = ""
        self.answer = ""
        self.font = font
        self.refresh_text_surface()
        self.screenSize = screenSize
        self.width = screenSize[0] / 4
        self.height = self.width * 2 / 3
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(0, self.height/5, self.width, self.height))
        self.image.fill((150, 150, 250), pygame.Rect(self.width/2 - self.height/10, 0, self.height/5, self.height/5))
        self.rect = pygame.Rect((screenSize[0] - self.width)/2, screenSize[1] - self.height, 0, 0)
        self.invaders = None
        self.speed = 3
        self.timerTicks = 0
    
    def set_question(self, question, answer):
        self.text = question[0]
        self.answer = answer
        self.refresh_text_surface()
        self.invaders = Invader(question[1], self.answer, self.font, self.screenSize)
    
    def refresh_text_surface(self):
        self.textSurface = self.font.render(self.text, True, (0,0,0))
        self.textRect = pygame.Rect((300 - self.textSurface.get_width())/2, (200 - self.textSurface.get_height())/2, 0, 0)
    
    def process_events(self):
        pass
    
    def update(self):
        self.timerTicks += 1
        if self.timerTicks > 60:
            self.speed += 1
            self.timerTicks = 0
        if self.invaders != None:
            self.invaders.move(self.speed)
        return self.invaders != None
    
    def is_complete(self):
        return self.invaders == None
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.textSurface, self.textRect)
        if self.invaders != None:
            self.invaders.draw(screen)