import os
import sys
import pygame
import random
from objects import *
from helpers import *
from generation import Generation
import numpy as np
import copy
import matplotlib.pyplot as plt

class Game():
  def __init__(self):
    pygame.init()

    self.generation = Generation()

    self.population = self.generation.population

    self.gamespeed = 4
    self.max_gamespeed = 10
    self.high_score = 0
    self.n_gen = 0
    self.current_gen_score = 0

    self.dinos = None
    self.genomes = []

    self.screen = pygame.display.set_mode(scr_size)
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Genetic T-Rex Rush')

    self.jump_sound = pygame.mixer.Sound('sprites/jump.wav')
    self.die_sound = pygame.mixer.Sound('sprites/die.wav')
    self.checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')

    self.scores = []
    self.fig = plt.figure(figsize=(int(width/100), 5))
    self.ax = plt.axes()
    plt.xlabel('Generation', fontsize=18)
    plt.ylabel('Score', fontsize=16)
    plt.show(block=False)

  def introscreen(self):
    Dino.containers = []
    temp_dino = Dino(44, 47, self.screen)
    temp_dino.isBlinking = True
    gameStart = False

    callout,callout_rect = load_image('call_out2.png',196,62,-1)
    callout_rect.left = width*0.05
    callout_rect.top = height*0.3

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('logo.png',240,40,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    logo2,logo2_rect = load_image('genetic_icon.png',80,80,-1)
    logo2 = logo2.convert_alpha()
    logo2_rect.centerx = width*0.45
    logo2_rect.centery = height*0.45

    while not gameStart:
      if pygame.display.get_surface() == None:
        print("Couldn't load display surface")
        return True
      else:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            return True
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
              temp_dino.isJumping = True
              temp_dino.isBlinking = False
              temp_dino.movement[1] = -temp_dino.jumpSpeed

      temp_dino.update()

      if pygame.display.get_surface() != None:
        self.screen.fill(background_col)
        self.screen.blit(temp_ground[0],temp_ground_rect)
        if temp_dino.isBlinking:
          self.screen.blit(logo2,logo2_rect)
          self.screen.blit(logo,logo_rect)
          self.screen.blit(callout,callout_rect)
        temp_dino.draw()

        pygame.display.update()

      self.clock.tick(FPS)
      if temp_dino.isJumping == False and temp_dino.isBlinking == False:
        gameStart = True

  def prepare(self):
    self.counter = 0
    self.gamespeed = 4
    self.current_gen_score = 0

    # load sprites
    self.new_ground = Ground(-self.gamespeed, self.screen)
    self.scb = Scoreboard(screen=self.screen)
    self.highsc = Scoreboard(width - 180, screen=self.screen)
    self.sursc = Scoreboard(width - 300, screen=self.screen)
    self.gensc = Scoreboard(width - 400, screen=self.screen)

    basicfont = pygame.font.SysFont('Menlo', 15)
    self.gen_text = basicfont.render('GEN', True, (0, 0, 0), background_col)
    self.textrect = self.gen_text.get_rect()
    self.textrect.top = height * 0.095
    self.textrect.left = width - 435

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    self.HI_image = pygame.Surface((22,int(11*6/5)))
    self.HI_rect = self.HI_image.get_rect()
    self.HI_image.fill(background_col)
    self.HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    self.HI_image.blit(temp_images[11],temp_rect)
    self.HI_rect.top = height*0.1
    self.HI_rect.left = width - 210

    temp_gen_image, self.gen_rect = load_sprite_sheet('dino.png',5,1,15,16,-1)
    self.gen_image = pygame.Surface((15, 16))
    self.gen_image.fill(background_col)
    self.gen_image.blit(temp_gen_image[0], self.gen_rect)
    self.gen_rect.top = height*0.08
    self.gen_rect.left = width - 320

    self.dinos = pygame.sprite.Group()
    Dino.containers = self.dinos
    for i in range(self.population):
      self.dinos.add(Dino(44,47, self.screen))
    if self.n_gen == 0:
      self.genomes = self.generation.set_initial_genomes()

    self.cacti = pygame.sprite.Group()
    self.pteras = pygame.sprite.Group()
    self.clouds = pygame.sprite.Group()
    self.last_obstacle = pygame.sprite.Group()
    self.all_obstacles = pygame.sprite.Group()

    Cactus.containers = self.cacti
    Ptera.containers = self.pteras
    Cloud.containers = self.clouds

  def update(self):
    # move self.cacti
    for c in self.cacti:
      c.movement[0] = -self.gamespeed
      for d in self.dinos:
        if pygame.sprite.collide_mask(d, c):
          d.isDead = True

    # move self.pteras
    for p in self.pteras:
      p.movement[0] = -self.gamespeed
      for d in self.dinos:
        if pygame.sprite.collide_mask(d, p):
          d.isDead = True

    # add more self.cacti
    if len(self.all_obstacles) == 0:
      new_object = Ptera(self.gamespeed, 46, 40, self.screen)

      self.all_obstacles.add(new_object)
      self.last_obstacle.empty()
      self.last_obstacle.add(new_object)
    elif len(self.all_obstacles) < 3:
      for l in self.last_obstacle:
        if l.rect.right < width * 0.7:
          r = random.randrange(0, 100)
          if r < 40:
            new_object = Cactus(self.gamespeed,40, 40, self.screen)
          elif r >= 40:
            new_object = Ptera(self.gamespeed, 46, 40, self.screen)

          self.all_obstacles.add(new_object)
          self.last_obstacle.empty()
          self.last_obstacle.add(new_object)

          break

    # add cloud
    if len(self.clouds) < 10 and random.randrange(0,100) == 10:
      Cloud(width,random.randrange(height/5,height/2), self.screen)

    # update motions
    self.dinos.update()
    self.cacti.update()
    self.pteras.update()
    self.clouds.update()
    self.new_ground.update()
    self.scb.update(self.current_gen_score)
    self.highsc.update(self.high_score)
    self.gensc.update(self.n_gen)
    self.sursc.update(self.n_survivors)

    # draw background
    if pygame.display.get_surface() != None:
      self.screen.fill(background_col)
      self.new_ground.draw()
      self.clouds.draw(self.screen)
      self.scb.draw()
      self.highsc.draw()
      self.screen.blit(self.HI_image,self.HI_rect)
      self.gensc.draw()
      self.screen.blit(self.gen_image, self.gen_rect)
      self.screen.blit(self.gen_text, self.textrect)
      self.sursc.draw()
      self.cacti.draw(self.screen)
      self.pteras.draw(self.screen)
      self.dinos.draw(self.screen)

      pygame.display.update()

    self.clock.tick(FPS)

    # make faster
    if self.counter % 70 == 69 and self.gamespeed < 10:
      self.new_ground.speed -= 0.05
      self.gamespeed += 0.05

    self.counter = (self.counter + 1)

  def gameplay(self):
    game_over = False

    self.prepare()

    print('===== %sth Generation =====' % self.n_gen)

    # game loop
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      # compute closest obstacle's distance
      first_obstacle = None
      obs_distance, obs_top, obs_bottom = width, 0, 0
      dino_rect_right = dino_position + 40
      for obs in self.all_obstacles:
        this_obs_distance = obs.rect.left - dino_position

        if this_obs_distance > 0 and this_obs_distance < obs_distance:
          obs_distance = this_obs_distance
          obs_top = obs.rect.top
          obs_bottom = obs.rect.bottom
          first_obstacle = obs

      # who are survived
      self.n_survivors = 0
      for di, dino in enumerate(self.dinos):
        # compute fitness
        self.genomes[di].fitness = dino.score

        if dino.isDead:
          continue

        # count survivors
        self.n_survivors += 1

        # decide action
        inputs = np.array([
          obs_distance / width,
          obs_top / height
        ], dtype=np.float32)
        outputs = self.genomes[di].forward(inputs)[0]
        # print(inputs, outputs)

        # execute action
        if outputs < 0: # do nothing
          dino.isDucking = False
        elif outputs < 0.5: # duck
          if not dino.isJumping and not dino.isDead:
            dino.isDucking = True
        else: # jump
          if dino.rect.bottom == int(0.98*height):
            dino.isJumping = True
            dino.movement[1] = -dino.jumpSpeed

        self.current_gen_score = dino.score

      # no survivors, kill this session
      if self.n_survivors == 0:
        if self.current_gen_score > self.high_score:
          self.high_score = self.current_gen_score

        game_over = True

      if game_over:
        break

      self.update()
      # end of while not game_over:

    # game over
    # crossover and mutate
    self.generation.set_genomes(self.genomes)
    self.generation.keep_best_genomes()
    self.genomes = self.generation.mutations()

    self.scores.append(self.current_gen_score)
    self.ax.plot(np.array(list(range(self.n_gen + 1))), np.array(self.scores), color='#225b85')
    self.fig.canvas.draw()
    self.fig.canvas.flush_events()

    print('Score: %s' % self.current_gen_score)

    # run next generation
    self.n_gen += 1
    self.gameplay()

    pygame.quit()
    exit()

  def start(self):
    isGameQuit = self.introscreen()
    if not isGameQuit:
      self.gameplay()

g = Game()
g.start()
