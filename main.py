import pygame
import random

pygame.font.init()
pygame.mixer.init()

#setting the screen
WIDTH, HEIGHT = 500, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 30)
FPS = 60
VEL = 5 
BULLET_VEL = 7
ALIEN_VEL = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 50
ALIEN_WIGTH, ALIEN_HEIGHT = 40, 25

SPACESHIP_IMAGE = pygame.image.load('assets/spaceship.png')
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

BULLET_IMAGE =  pygame.image.load('assets/bullet.png')
BULLET = pygame.transform.scale(BULLET_IMAGE, (18,30))

ENEMY_BULLET_IMAGE = pygame.image.load('assets/bulletalien.webp')
ENEMY_BULLET = pygame.transform.scale(ENEMY_BULLET_IMAGE, (18, 30))

ENEMY_IMAGE = pygame.image.load('assets/alienship.png')
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ALIEN_WIGTH, ALIEN_HEIGHT))

SPACE_IMAGE =  pygame.image.load('assets/space.jpeg')
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

HEART_IMAGE = pygame.image.load('assets/heart.png')
HEART = pygame.transform.scale(HEART_IMAGE, (40, 25))

BULLET_SOUND = pygame.mixer.Sound('assets/Gun+Silencer.mp3')
BULLET_SOUND.set_volume(0.2)
VICTORY_SOUND = pygame.mixer.Sound('assets/victory.mp3')
VICTORY_SOUND.set_volume(0.5)
DEATH_SOUND = pygame.mixer.Sound('assets/explosion.mp3')
DEATH_SOUND.set_volume(0.2)
ENEMY_BULLET_SOUND = pygame.mixer.Sound('assets/laser.mp3')
ENEMY_BULLET_SOUND.set_volume(0.2)
GAME_OVER_SOUND = pygame.mixer.Sound('assets/gameover.mp3')


ALIEN_HIT = pygame.USEREVENT + 1
ALIEN_MOVE_EVENT = pygame.USEREVENT + 2
ALIEN_MOVE_INTERVAL = 500
PLAYER_HIT = pygame.USEREVENT + 3


def draw_window(player, bullets, aliens, score, enemy_bullets, lives):

    WINDOW.blit(SPACE, (0,0))

    WINDOW.blit(SPACESHIP, (player.x, player.y))

    score_text = FONT.render(str(score), 1, WHITE)
    WINDOW.blit(score_text, (10, HEIGHT-40))

    #Mostrar alien
    for alien in aliens:
        WINDOW.blit(ENEMY, (alien.x, alien.y))
    
    #mostrar Lives
    for live in lives:
        WINDOW.blit(HEART, (live.x, live.y))

    #mostrar Bullets
    for bullet in bullets:
        WINDOW.blit(BULLET, (bullet.x ,bullet.y))
    
    #mostrar EnemyBullets
    for bullet in enemy_bullets:
        WINDOW.blit(ENEMY_BULLET, (bullet.x, bullet.y))
    
    pygame.display.update()


def enemy_bullets_movement(enemy_bullets, player):
    for bullet in enemy_bullets:
        bullet.y += BULLET_VEL

        if player.colliderect(bullet): #Se verifica si hay una colisión entre la bala y el jugador utilizando el método colliderect(). Si hay una colisión, significa que la bala ha alcanzado al jugador.
            enemy_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER_HIT))


def bullet_movement(bullets, aliens):
    aliens_to_remove = []

    for bullet in bullets:
        bullet.y -= BULLET_VEL
        for alien in aliens:
            if alien.colliderect(bullet) and alien.y > -15:
                bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(ALIEN_HIT))
                aliens_to_remove.append(alien)
    
    for alien in aliens_to_remove:
        aliens.remove(alien)


def spaceship_movement(keys_pressend, player):
    if keys_pressend[pygame.K_LEFT] and player.x - VEL > 0:
        player.x -= VEL
    if keys_pressend[pygame.K_RIGHT] and player.x + VEL < WIDTH - SPACESHIP_WIDTH:
        player.x += VEL


def create_enemy_bullet(aliens):
    if len(aliens) > 0:
        random_alien = random.choice(aliens)
        bullet = pygame.Rect(random_alien.x, random_alien.y, 10, 5)
        return bullet
    else:
        pass


ALIEN_DIRECTION = 1

def alien_movement(aliens):
    global ALIEN_DIRECTION
    for alien in aliens:
        alien.y += ALIEN_VEL

    if ALIEN_DIRECTION == 1:
        for alien in aliens:
            alien.x += ALIEN_VEL
        ALIEN_DIRECTION = -1
    else:
        for alien in aliens:
            alien.x -= ALIEN_VEL
        ALIEN_DIRECTION = 1

def draw_victory():
    VICTORY_SOUND.play()
    victory_text = FONT.render('YOU WIN!', 1, WHITE)
    WINDOW.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - victory_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)    

def draw_game_over():
    game_over_text = FONT.render('GAME OVER', 1, WHITE)
    WINDOW.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
    pygame.display.update()  # Actualizar la pantalla para mostrar el mensaje "Game Over"
    pygame.time.delay(3000)   # Pausar la ejecución del programa durante 3 segundos 



def main():
    player = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH, HEIGHT - SPACESHIP_HEIGHT - 50, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    #  Este objeto se utiliza para controlar la velocidad de actualización del juego, es decir, cuántas veces se actualiza el juego por segundo. 
    clock = pygame.time.Clock()

    enemy_bullets = []
    score = 0
    bullets = []
    aliens = []
    lives = []

    for i in range(8):
        for j in range(50):
            alien = pygame.Rect(50 * i + 50, -50 * j + 50, ALIEN_WIGTH, ALIEN_HEIGHT)
            aliens.append(alien)

    for i in range(3):
        x = 45 * i
        live = pygame.Rect(350 + x, 660, 40, 25)
        lives.append(live)

    run = True

    # Configurar el temporizador
    pygame.time.set_timer(ALIEN_MOVE_EVENT, ALIEN_MOVE_INTERVAL)

    while run:
        ## Limitar la velocidad del juego a 60 FPS
        clock.tick(FPS)

        for alien in aliens:
            if alien.y > HEIGHT - 130:
                GAME_OVER_SOUND.play()
                draw_game_over()
                run = False
                break
        
        #En resumen, este bloque de código maneja el evento de cerrar la ventana del juego, permitiendo que el jugador cierre el juego de manera adecuada y segura.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #cerrar la ventana y salir de pygame limpiamente
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.x + player.width//2 - 2, player.y, 10, 5)
                    bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == ALIEN_HIT:
                score += 100
                if len(aliens) == 0:
                    draw_victory()
                    run = False
                    break

            if event.type == ALIEN_MOVE_EVENT:
                alien_movement(aliens)

                if random.randint(1, 1) == 1:
                    enemy_bullets.append(create_enemy_bullet(aliens))
                    ENEMY_BULLET_SOUND.play()

            if event.type == PLAYER_HIT:
                if len(lives) > 1:
                    DEATH_SOUND.play()
                    lives.pop()
                else:
                    GAME_OVER_SOUND.play()
                    draw_game_over()
                    run = False
                    break

        
        keys_pressed = pygame.key.get_pressed()
        spaceship_movement(keys_pressed, player)
        bullet_movement(bullets, aliens)
        enemy_bullets_movement(enemy_bullets, player)
        draw_window(player, bullets, aliens, score, enemy_bullets, lives)
    

if __name__ == "__main__":
    main()
