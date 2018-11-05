import os
import sys
import pygame
import random
from helpers import *

class Dino(pygame.sprite.Sprite):
  def __init__(self, sizex=-1, sizey=-1, screen=None):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.images,self.rect = load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
    self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
    self.rect.bottom = int(0.98*height)
    self.rect.left = dino_position
    self.image = self.images[0]
    self.index = 0
    self.counter = 0
    self.score = 0
    self.isJumping = False
    self.isDead = False
    self.isDucking = False
    self.isBlinking = False
    self.movement = [0,0]
    self.jumpSpeed = 11

    self.fitness = 0

    self.stand_pos_width = self.rect.width
    self.duck_pos_width = self.rect1.width

    self.screen = screen

  def draw(self):
    self.screen.blit(self.image,self.rect)

  def checkbounds(self):
    if self.rect.bottom > int(0.98*height):
      self.rect.bottom = int(0.98*height)
      self.isJumping = False

  def update(self):
    if self.isDead:
      self.index = 4
      self.image = self.images[self.index]
      self.rect.width = self.stand_pos_width
      self.image.set_alpha(0)
      return

    if self.isJumping:
      self.movement[1] = self.movement[1] + gravity
      self.index = 0

    elif self.isBlinking:
      if self.index == 0:
        if self.counter % 200 == 199:
          self.index = (self.index + 1)%2
      else:
        if self.counter % 20 == 19:
          self.index = (self.index + 1)%2

    elif self.isDucking:
      if self.counter % 5 == 0:
        self.index = (self.index + 1)%2

    else:
      if self.counter % 5 == 0:
        self.index = (self.index + 1)%2 + 2

    if not self.isDucking:
      self.image = self.images[self.index]
      self.rect.width = self.stand_pos_width
    else:
      self.image = self.images1[(self.index)%2]
      self.rect.width = self.duck_pos_width

    self.rect = self.rect.move(self.movement)
    self.checkbounds()

    if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
      self.score += 1
    #   if self.score % 100 == 0 and self.score != 0:
    #     if pygame.mixer.get_init() != None:
    #       self.checkPoint_sound.play()

    self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
  def __init__(self,speed=5,sizex=-1,sizey=-1, screen=None):
    pygame.sprite.Sprite.__init__(self,self.containers)
    self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
    self.rect.bottom = int(0.98*height)
    self.rect.left = width + self.rect.width
    self.image = self.images[random.randrange(0,3)]
    self.movement = [-1*speed,0]

    self.screen = screen

  def draw(self):
    self.screen.blit(self.image,self.rect)

  def update(self):
    self.rect = self.rect.move(self.movement)

    if self.rect.right < 0:
      self.kill()

class Ptera(pygame.sprite.Sprite):
  def __init__(self,speed=5,sizex=-1,sizey=-1, screen=None):
    pygame.sprite.Sprite.__init__(self,self.containers)
    self.images,self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
    self.ptera_height = [height*0.82, height*0.55]
    self.rect.centery = self.ptera_height[random.randrange(0,2)]
    self.rect.left = width + self.rect.width
    self.image = self.images[0]
    self.movement = [-1*speed,0]
    self.index = 0
    self.counter = 0

    self.screen = screen

  def draw(self):
    self.screen.blit(self.image,self.rect)

  def update(self):
    if self.counter % 10 == 0:
      self.index = (self.index+1)%2
    self.image = self.images[self.index]
    self.rect = self.rect.move(self.movement)
    self.counter = (self.counter + 1)
    if self.rect.right < 0:
      self.kill()


class Ground():
  def __init__(self,speed=-5, screen=None):
    self.image,self.rect = load_image('ground.png',-1,-1,-1)
    self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
    self.rect.bottom = height
    self.rect1.bottom = height
    self.rect1.left = self.rect.right
    self.speed = speed

    self.screen = screen
  def draw(self):
    self.screen.blit(self.image,self.rect)
    self.screen.blit(self.image1,self.rect1)

  def update(self):
    self.rect.left += self.speed
    self.rect1.left += self.speed

    if self.rect.right < 0:
      self.rect.left = self.rect1.right

    if self.rect1.right < 0:
      self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
  def __init__(self,x,y, screen=None):
    pygame.sprite.Sprite.__init__(self,self.containers)
    self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
    self.speed = 1
    self.rect.left = x
    self.rect.top = y
    self.movement = [-1*self.speed,0]

    self.screen = screen

  def draw(self):
    self.screen.blit(self.image,self.rect)

  def update(self):
    self.rect = self.rect.move(self.movement)
    if self.rect.right < 0:
      self.kill()

class Scoreboard():
  def __init__(self,x=-1,y=-1, screen=None):
    self.score = 0
    self.tempimages,self.temprect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    self.image = pygame.Surface((55,int(11*6/5)))
    self.rect = self.image.get_rect()
    if x == -1:
      self.rect.left = width*0.89
    else:
      self.rect.left = x
    if y == -1:
      self.rect.top = height*0.1
    else:
      self.rect.top = y

    self.screen = screen

  def draw(self):
    self.screen.blit(self.image,self.rect)

  def update(self,score):
    score_digits = extractDigits(score)
    self.image.fill(background_col)
    for s in score_digits:
      self.image.blit(self.tempimages[s],self.temprect)
      self.temprect.left += self.temprect.width
    self.temprect.left = 0