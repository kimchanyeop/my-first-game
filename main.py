import  math ,sys, random
import pygame as pg
from pygame import key
from pygame.locals import *

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode([700,700])
pg.display.set_caption('space shooter')
pg.mouse.set_visible(False)

def load_image(path):
  return pg.image.load(path).convert_alpha()

def random_spawn():
  y = random.randint(-100, 0)
  x = random.randint(0, 700)
  return [x,y]
  

class enemy:
  total = 8
  def __init__(self, pos):
    self.img = load_image('images/enemy.png')
    self.loc = pos
    self.speed = random.randint(3,10)
    self.rect = pg.Rect(self.loc[0],self.loc[1],60,60)
    self.dead = False
    self.is_hit = False
    
    
  def update(self):
    self.loc[1] += self.speed
    self.rect = pg.Rect(self.loc[0],self.loc[1],60,60)
    screen.blit(self.img,(self.loc[0],self.loc[1]))
          
player_img = load_image('images/player.png')
gun_img = load_image('images/gun.png')
pointer_img = load_image('images/pointer.png')
bullet_img = load_image('images/bullet.png')
shooting_sound = pg.mixer.Sound('images/piew.wav')
player_location = [350,350]
player_rect = pg.Rect(player_location[0],player_location[1],60,60)
moving_right = False
moving_left = False
moving_up = False
moving_down = False
bullet_pos = []
fire_angle = []
click = False
bullet_speed = 20
font = pg.font.Font(None, 30)
test = []
alive = True
fire_rate_timer = 30
enemy_health = 2
spawn_timer = 0
enemies = []
game_over = False
point = 0

for i in range(enemy.total):
  enemies.append(enemy(random_spawn()))
while True:
  screen.fill((0,0,0))
  player_hitbox = pg.Rect(player_location[0]-30,player_location[1]-30,60,60)
  fire_rate_timer += 2 

  mouse_x, mouse_y = pg.mouse.get_pos()
  rel_x, rel_y = mouse_x - player_location[0], mouse_y - player_location[1]
  angle = -math.degrees(math.atan2(rel_y,rel_x))
  
  
  bullet_pos = [[pos[0]+bullet_speed*math.cos(math.radians(pos[2])), pos[1]-bullet_speed*math.sin(math.radians(pos[2])), pos[2] ] for pos in bullet_pos]
  
  
  screen.blit(player_img,(player_location[0]-30, player_location[1]-30))
  for e in enemies:
    e.update()
    if player_hitbox.colliderect(e.rect):
        game_over = True
        
        
        
  for bullet_x, bullet_y, fire_angle in bullet_pos:
    bullet_rect = pg.Rect(bullet_x, bullet_y, 2,2)
    screen.blit(bullet_img,(bullet_x,bullet_y))
    if bullet_x < 0 or bullet_x > 700 or bullet_y < 0 or bullet_y > 700:
      bullet_pos.remove(bullet_pos[0])
    for e in enemies[:]:
      if bullet_rect.colliderect(e.rect):
        enemies.remove(e)
        enemies.append(enemy(random_spawn()))
        point += 10
      if e.loc[1] > 700:
        enemies.remove(e)
        enemies.append(enemy(random_spawn()))
      if player_hitbox.colliderect(e.rect):
        game_over = True
      

  gun_img_copy = pg.transform.rotate(gun_img, int(angle))
  screen.blit(gun_img_copy,(player_location[0]-int(gun_img_copy.get_width()/2), player_location[1]-int(gun_img_copy.get_height()/2)))
  textsurface = font.render(str(point), False, (255, 255, 255))
  screen.blit(textsurface,(300,0))
  screen.blit(pointer_img,(mouse_x-16,mouse_y-16))
  fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
  screen.blit(fps,(0,0))
  if game_over == True:
    screen.fill((0,0,0))
    textsurface = font.render('your score is: '+ str(point), False, (255, 255, 255))
    screen.blit(textsurface,(300,350))
  

  if moving_right == True:
    player_location[0] += 4
  elif moving_left == True:
    player_location[0] -= 4
  elif moving_up == True:
    player_location[1] -= 4   
  elif moving_down == True:
    player_location[1] += 4

  if player_hitbox.x > 700:
    player_location[0] = 670
  elif player_hitbox.x < 0:
    player_location[0] = 30
  elif player_hitbox.y > 700:
    player_location[1]  = 670
  elif player_hitbox.y < 0:
    player_location[1] = 30


  for event in pg.event.get():
    if event.type == QUIT:
      pg.quit()
      sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_d:
        moving_right = True
      elif event.key == K_a:
        moving_left = True
      elif event.key == K_w:
        moving_up = True
      elif event.key == K_s:
        moving_down = True
    if event.type == KEYUP:
      if event.key == K_d:
        moving_right = False
      elif event.key == K_a:
        moving_left = False
      elif event.key == K_w:
        moving_up = False
      elif event.key == K_s:
        moving_down = False
    
  if fire_rate_timer > 30:
    fire_rate_timer = 30
    if event.type == MOUSEBUTTONDOWN:
      bullet_x, bullet_y, fire_angle = player_location[0], player_location[1], angle
      bullet_pos.append([player_location[0], player_location[1], fire_angle])        
      click = True
      fire_rate_timer = 0
      shooting_sound.play()
  
  
  pg.display.update()
  clock.tick(60)


       
    
