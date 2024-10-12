import pygame
from pygame.math import Vector2
import random, sys, random, os

CELL_NUMBER = 27
CELL_SIZE = 24

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
file = "snake/"

score_text = pygame.font.Font(file + "Font/ARIAL.TTF", 28)

class FRUIT() :
    
    fruit = pygame.image.load(file + "Assets/apple/fruit.png").convert_alpha()
    
    def __init__(self) :
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
        FRUIT.fruit = pygame.transform.scale(FRUIT.fruit, (CELL_SIZE, CELL_SIZE))

    def randomize(self) :
        
        prev_pos = self.pos
        while prev_pos == self.pos :
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
            
    def draw(self) :
        fruit_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        screen.blit(FRUIT.fruit, fruit_rect)

class SNAKE() :
    
    def __init__(self) :
        self.x = random.randint(0, CELL_NUMBER - 3)
        self.y = random.randint(0, CELL_NUMBER - 3)
        
        self.body = [Vector2(self.x, self.y), Vector2(self.x + 1, self.y), Vector2(self.x + 2, self.y)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.first = False

        self.utils = []
        self.snake_utils()
        

    def snake_utils(self) :
        
        images = []

        for root, dirs, files in os.walk(file + '/Assets/snake', topdown=True):
            images = files
        for i in range(len(images)) :
            name = files[i][:-4]
            name = pygame.image.load(root + '/' + files[i]).convert_alpha()
            name = pygame.transform.scale(name, (CELL_SIZE, CELL_SIZE))
            
            self.utils.append(name)

    def draw(self) :

        for index, block in enumerate(self.body) :
            block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if index == 0 :

                if   self.direction == Vector2(0, 1)  : screen.blit(self.utils[2], block_rect)
                elif self.direction == Vector2(-1, 0) : screen.blit(self.utils[3], block_rect)
                elif self.direction == Vector2(0, 0)  : screen.blit(self.utils[3], block_rect)
                elif self.direction == Vector2(1, 0)  : screen.blit(self.utils[4], block_rect)
                elif self.direction == Vector2(0, -1) : screen.blit(self.utils[5], block_rect)
            
            elif index == len(self.body) -1 :

                if   (self.body[-2] - self.body[-1]) == Vector2(0, 1)  : screen.blit(self.utils[13], block_rect)
                elif (self.body[-2] - self.body[-1]) == Vector2(-1, 0) : screen.blit(self.utils[12], block_rect)
                elif (self.body[-2] - self.body[-1]) == Vector2(0, 0)  : screen.blit(self.utils[12], block_rect)
                elif (self.body[-2] - self.body[-1]) == Vector2(1, 0)  : screen.blit(self.utils[11], block_rect)
                elif (self.body[-2] - self.body[-1]) == Vector2(0, -1) : screen.blit(self.utils[10], block_rect)

            else :
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                if prev_block.x == next_block.x   : screen.blit(self.utils[0], block_rect)
                elif prev_block.y == next_block.y : screen.blit(self.utils[1], block_rect)
                else :
                    if   prev_block.x == 1  and next_block.y ==  1 or prev_block.y ==  1  and next_block.x ==  1 : screen.blit(self.utils[8], block_rect)
                    elif prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1  and next_block.x == -1 : screen.blit(self.utils[7], block_rect)
                    elif prev_block.x == -1 and next_block.y ==  1 or prev_block.y ==  1  and next_block.x == -1 : screen.blit(self.utils[9], block_rect)
                    elif prev_block.x == 1  and next_block.y == -1 or prev_block.y == -1  and next_block.x ==  1 : screen.blit(self.utils[6], block_rect)

    def move_snake(self) :
        if self.new_block == True :

            copy_block = self.body[:]
            copy_block.insert(0, copy_block[0] + self.direction)
            self.body = copy_block[:]
            self.new_block = False
        
        else :
            if self.first :
                copy_block = self.body[: -1]
                copy_block.insert(0, copy_block[0] + self.direction)
                self.body = copy_block[:]
    

class GAME() :

    def __init__(self) :
        self.Snake = SNAKE()
        self.Fruit = FRUIT()
        self.game_over = False
        self.crunch_sound = pygame.mixer.Sound(file + "Sound/crunch_sound.mp3")
    
    def Grass(): 
        grass_color = (169, 206, 61)
        for row in range(CELL_NUMBER) : 
            if row % 2 == 0 :
                for col in range(CELL_NUMBER) : 
                    if col % 2 == 0 :
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
        
            else :
                for col in range(CELL_NUMBER) : 
                    if col % 2 != 0 :
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                
    def Draw(self) :
        
        GAME.Grass()
        self.Snake.draw()
        self.Fruit.draw()
        self.draw_text()
        
    def update(self) :
        self.Snake.move_snake()
        self.Logic()
    
    def Logic(self) :

        if self.Snake.body[0] == self.Fruit.pos :
            self.Fruit.randomize()
            self.Snake.new_block = True
            self.crunch_sound.play()
        if not 0 <= self.Snake.body[0].x <= CELL_NUMBER - 1 or not 0 <= self.Snake.body[0].y <= CELL_NUMBER - 1 :
            self.game_over = True 
    
    def draw_text(self) :

        score = str(len(self.Snake.body) - 3) 
        score_surface = score_text.render(score, True, (0, 0, 0))
        score_rect = score_surface.get_rect(center = (CELL_NUMBER * CELL_SIZE - 60, CELL_NUMBER * CELL_SIZE - 40))
        
        if int(score) < 10 :
            apple_rect = score_surface.get_rect(midright= (score_rect.left - 15, score_rect.centery +2))
            bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 20, apple_rect.height + -2)

        else :
            apple_rect = score_surface.get_rect(midright= (score_rect.left + 2, score_rect.centery))
            bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)

        screen.blit(score_surface, score_rect)
        screen.blit(self.Fruit.fruit, apple_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 1)
    

def main() : 
    Game = GAME()

    while not Game.game_over :

        for event in pygame.event.get() :

            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

            if event.type == SCREEN_UPDATE :
                Game.update()

            elif event.type == pygame.KEYUP :

                Game.Snake.first = True

                if event.key == pygame.K_UP :
                    if not Game.Snake.direction == Vector2(0, 1) :
                        Game.Snake.direction = Vector2(0, -1)

                elif event.key == pygame.K_DOWN :
                    if not Game.Snake.direction == Vector2(0, -1) :
                        Game.Snake.direction = Vector2(0, 1)

                elif event.key == pygame.K_RIGHT :
                    if not Game.Snake.direction == Vector2(-1, 0) :
                        Game.Snake.direction = Vector2(1, 0)

                elif event.key == pygame.K_LEFT :
                    if not Game.Snake.direction == Vector2(1, 0) :
                        Game.Snake.direction = Vector2(-1, 0)


        screen.fill((175, 215, 70))
        Game.Draw()

        pygame.display.update()

        CLOCK.tick(60)

if __name__ =="__main__" :
    main()