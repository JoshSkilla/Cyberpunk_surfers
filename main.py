import pygame
import random
from time import time, sleep
file = 'music.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()


WHITE = (255, 255, 255)

SCREEN_HEIGHT = 350
SCREEN_WIDTH = 500

run_ani = [pygame.image.load("run1.png"), pygame.image.load("run2.png"),
             pygame.image.load("run3.png"),pygame.image.load("run4.png"),
             pygame.image.load("run5.png"),pygame.image.load("run6.png")]

gem_ani = [pygame.image.load("gem1.png"), pygame.image.load("gem2.png"),
             pygame.image.load("gem3.png"),pygame.image.load("gem4.png")]

label = 'Distance: 0'
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 15)

textRect = font.render(label, True, "green").get_rect()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#def cronos():


class MasterSprite(pygame.sprite.Sprite):
    def __init__(self, imageFile, x=0, y=0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(imageFile)
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.displaySize = pygame.display.get_surface().get_size()
        self.width = self.rect.right - self.x
        self.height = self.rect.bottom - self.y

    def getRect(self):
        return self.rect

    def getSurface(self):
        return self.image

    def move(self):
        pass

    def setX(self, x):
        self.x = x
        self.rect.x = x

    def setXY(self,x,y):
        self.setX(x)
        self.setY(y)

    def setY(self, y):
        self.y = y
        self.rect.y = y

class Player(MasterSprite):
  def __init__(self,x,y):
    super().__init__("run1.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0
    self.jumpCount = 7
    self.vel = 5
    self.jumping = False
    self.dead = False
    self.running = True
    self.move_frame = 0
    self.ground = 35

  def move(self,x,y):
    self.changeY = y

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)
    if self.move_frame > 5:
        self.move_frame = 0
        return

    if self.jumping == False and self.running == True and self.dead == False:
        self.image = run_ani[self.move_frame]
        self.move_frame += 1
    else:
        if self.dead == True:
            self.image = pygame.image.load("dead.png")

class Background(MasterSprite):
  def __init__(self,x,y):
    super().__init__("background.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0

  def move(self,x,y):
    self.changeX = x

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)


class Train(MasterSprite):
  def __init__(self,x,y):
    super().__init__("train.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0
    self.level = 0
    self.speed = -12

  def move(self,x,y):
    self.changeX = x

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)

class Gem(MasterSprite):
  def __init__(self,x,y):
    super().__init__("gem1.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0
    self.level = 0
    self.speed = -6.34
    self.move_frame = 0
    self.hide = False

  def move(self,x,y):
    self.changeX = x

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)
    if self.hide == False:
        if self.move_frame > 3:
            self.move_frame = 0


        self.image = gem_ani[round(self.move_frame)]
        self.move_frame += 0.1
    else:
        self.image = pygame.image.load("hide.png")

class Game_over(MasterSprite):
    def __init__(self, x, y):
        super().__init__("game_over.png")
        self.originalImage = self.image
        self.setXY(x, y)
        self.changeX = 0
        self.changeY = 0
        self.level = 0
        self.speed = 0

    def move(self, x, y):
        self.changeX = x

    def update(self):
        self.setXY(self.x + self.changeX, self.y + self.changeY)

class Collision(MasterSprite):
  def __init__(self,x,y):
    super().__init__("collision1.png")
    self.originalImage = self.image
    self.setXY(x,y)
    self.changeX = 0
    self.changeY = 0

  def move(self,x,y):
    self.changeX = x

  def update(self):
    self.setXY(self.x+self.changeX, self.y+self.changeY)



def main():

    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Cyberpunk Surfers")

    clock = pygame.time.Clock()
    background = Background(0,0)
    player = Player(35,275)
    collision = Collision(375,278)
    train =  Train(375,275)
    game_over = Game_over(125, -115)
    gem = Gem(540,285)


    run = True

    clock = pygame.time.Clock()
    minutes = 0
    seconds = 0
    score = 0
    milliseconds = 0

    while run:
        if milliseconds > 30 and player.dead == False:
            seconds += 1
            milliseconds -= 30
        milliseconds += clock.tick_busy_loop(60)
        label = 'Distance: ' + str(seconds) + '                                                                                   Score: ' +str(score)

        rect1 = player.getRect()
        rect2 = collision.getRect()
        rect3 = train.getRect()
        rect4 = gem.getRect()
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
        keys = pygame.key.get_pressed()
        if player.jumping == False:
            if player.y < 275 and rect1.colliderect(rect3) == False:
                player.y += 5
            if keys[pygame.K_SPACE] and player.dead == False:
                player.jumping = True
        else:
            neg = 1
            if player.jumpCount < -7 or (player.jumpCount <= -7 and rect1.colliderect(rect3) == True):
                player.jumping = False
                player.jumpCount = 7
                if player.y <275 and rect1.colliderect(rect3) == False:
                    player.y = 275
            else:
                if player.jumpCount < 0:
                    neg = -1
                player.y -= (neg*0.5*(player.jumpCount**2))
                player.jumpCount -=1

        if background.x <-633:
            background.x = 0
        else:
            if player.dead == False:
                if rect1.colliderect(rect2) == True:
                    player.dead = True
                    player.image = pygame.image.load("dead.png")
                    background.move(0, 0)
                    train.move(0, 0)
                    collision.move(0,0)
                    gem.move(0,0)
                    #player.changeX = -6.34
                    #player.changeX = -2.34
                else:
                    background.move(-6.34,0)
                    if train.x <-300:
                        train.level += 1
                        train.speed = random.randint(-12-train.level,-6)*1.5
                        train.x = 500
                        collision.x = 500
                    else:
                        train.move(train.speed,0)
                        collision.move(train.speed,0)

                    gem.move(gem.speed, 0)
                    if rect1.colliderect(rect4) == True:
                        score+=1
                        gem.hide=True
                        gem.y=100
                    elif gem.x<-60:
                        gem.x = 550
                        gem.y = random.randint(180,269)
                        gem.hide=False



            else:
                background.move(0, 0)
                train.move(0, 0)
                gem.move(0, 0)
                collision.move(0, 0)
                pygame.mixer.music.stop()
                game_over.x = 125
                game_over.y=87





        screen.fill(WHITE)


        background.update()
        gem.update()
        player.update()
        train.update()
        collision.update()
        game_over.update()

        screen.blit(background.getSurface(), background.getRect())
        screen.blit(gem.getSurface(), gem.getRect())
        screen.blit(player.getSurface(), player.getRect())

        screen.blit(train.getSurface(), train.getRect())
        screen.blit(collision.getSurface(), collision.getRect())
        screen.blit(game_over.getSurface(), game_over.getRect())
        screen.blit(font.render(label, True, "green"), textRect)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
  main()
