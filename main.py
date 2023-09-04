import pygame 
import os 

pygame.font.init() 
pygame.mixer.init() 

WIDTH, HEIGHT = 900, 500 
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
WHITE, BLACK, YELLOW, RED = (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 0, 0) 
FPS = 60 
SCALE_WIDTH, SCALE_HEIGHT = 50, 40 
VELOCITY = 5 
BORDER_WIDTH = 10 
BORDER = pygame.Rect(WIDTH / 2 - BORDER_WIDTH / 2, 0, BORDER_WIDTH, HEIGHT) 
BULLET_WIDTH, BULLET_HEIGHT = 10, 6
MAX_BULLETS = 3 
BULLET_VELOCITY = 10 
YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2 
GAME_FONT = pygame.font.SysFont('comicsans', 35) 

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT)) 

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png' )) 
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SCALE_WIDTH, SCALE_HEIGHT)), 90) 

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png' )) 
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SCALE_WIDTH, SCALE_HEIGHT)), -90) 

BULLET_COLLISION_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3')) 
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3')) 

pygame.display.set_caption('Star Wars') 

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health): 
  WIN.blit(SPACE_BACKGROUND, (0, 0)) 
  pygame.draw.rect(WIN, BLACK, BORDER) 

  yellow_health_text = GAME_FONT.render('HEALTH: ' + str(yellow_health), 1, WHITE) 
  red_health_text = GAME_FONT.render('HEALTH: ' + str(red_health), 1, WHITE) 

  WIN.blit(yellow_health_text, (10, 10)) 
  WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) 

  for bullet in yellow_bullets: 
    pygame.draw.rect(WIN, YELLOW, bullet) 

  for bullet in red_bullets:
    pygame.draw.rect(WIN, RED, bullet) 

  WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) 
  WIN.blit(RED_SPACESHIP, (red.x, red.y)) 
  pygame.display.update() 

def yellow_handle_movement(keys_pressed, yellow): 
  if keys_pressed[pygame.K_a] and yellow.x > VELOCITY: 
    yellow.x -= VELOCITY 
  if keys_pressed[pygame.K_d] and BORDER.x - yellow.width > yellow.x + VELOCITY: 
    yellow.x += VELOCITY 
  if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: 
    yellow.y -= VELOCITY 
  if keys_pressed[pygame.K_s] and yellow.y + VELOCITY < HEIGHT - yellow.height: 
    yellow.y += VELOCITY 

def red_handle_movement(keys_pressed, red):
  if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER_WIDTH: 
    red.x -= VELOCITY 
  if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY < WIDTH - red.width: 
    red.x += VELOCITY 
  if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: 
    red.y -= VELOCITY 
  if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY < HEIGHT - red.height: 
    red.y += VELOCITY 

def handlebullet(yellow, red, yellow_bullets, red_bullets):
  for bullet in yellow_bullets:
    bullet.x += BULLET_VELOCITY 
    if red.colliderect(bullet):
      pygame.event.post(pygame.event.Event(RED_HIT)) 
      yellow_bullets.remove(bullet) 
    if bullet.x > WIDTH + BULLET_WIDTH:
      yellow_bullets.remove(bullet) 

  for bullet in red_bullets:
    bullet.x -= BULLET_VELOCITY 
    if yellow.colliderect(bullet):
      pygame.event.post(pygame.event.Event(YELLOW_HIT)) 
      red_bullets.remove(bullet) 
    if bullet.x < 0 - BULLET_WIDTH:
      red_bullets.remove(bullet) 

def handle_winner(text):
  draw_text = GAME_FONT.render(text, 1, WHITE) 
  WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2)) 
  pygame.display.update() 
  pygame.time.delay(5000) 

def main(): 
  yellow = pygame.Rect(200, 100, SCALE_WIDTH, SCALE_HEIGHT) 
  red = pygame.Rect(700, 100, SCALE_WIDTH, SCALE_HEIGHT) 

  yellow_bullets, red_bullets = [], [] 
  yellow_health, red_health = 5, 5 

  clock = pygame.time.Clock() 
  run = True  
  while run: 
    clock.tick(FPS) 
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
        run = False 
        pygame.quit() 

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
          bullet = pygame.Rect(yellow.x + yellow.w, yellow.y + yellow.height / 2 - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT) 
          yellow_bullets.append(bullet) 
          BULLET_FIRE_SOUND.play() 

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
          bullet = pygame.Rect(red.x, red.y + red.height / 2 - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT) 
          red_bullets.append(bullet) 
          BULLET_FIRE_SOUND.play() 

      if event.type == RED_HIT:
        red_health -= 1 
        BULLET_COLLISION_SOUND.play() 

      if event.type == YELLOW_HIT: 
        yellow_health -= 1 
        BULLET_COLLISION_SOUND.play() 

    win_text = "" 

    if yellow_health <= 0: 
      win_text = "RED WON!" 

    if red_health <= 0: 
      win_text = "YELLOW WON!" 

    if win_text != "": 
      handle_winner(win_text) 
      break 

    keys_pressed = pygame.key.get_pressed() 

    yellow_handle_movement(keys_pressed, yellow) 
    red_handle_movement(keys_pressed, red) 

    handlebullet(yellow, red, yellow_bullets, red_bullets) 

    draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health) 

  main() 

if __name__ == "__main__": 
  main() 