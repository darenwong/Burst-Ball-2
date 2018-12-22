import pygame
import math
import random

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class ball:
    def __init__(self, x, y, r, a, b):
        self.x = x
        self.y = y
        self.r = r
        self.v = random.randint(0,400)/1000
        self.a = a
        self.b = b
        self.color = (120, 255 - int(self.r), self.r)
    
    def move(self, dt):
        self.x += self.v*dt*math.sin(self.a)
        self.y -= self.v*dt*math.cos(self.a)
    
    def wall_coll(self):

        if self.x > screen_width - self.r:
            self.x = 2*(screen_width - self.r) - self.x
            self.a = - self.a
            self.b = self.b -1 
            
        elif self.x < self.r:
            self.x = 2*self.r - self.x
            self.a = - self.a
            self.b = self.b -1 
            
        if self.y > screen_height - self.r:
            self.y = 2*(screen_height - self.r) - self.y
            self.a = math.pi - self.a
            self.b = self.b -1 
     
        elif self.y < self.r:
            self.y = 2*self.r - self.y
            self.a = math.pi - self.a     
            self.b = self.b -1 
        
    def check_ball_point(self):
        if self.b <= 0:
            return True
        else:
            return False

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r))
        font = pygame.font.SysFont(None, int(self.r*2))
        text = font.render(str(self.b), True, WHITE)
        textsize = text.get_rect()
        textsize.center = (int(self.x), int(self.y))
        screen.blit(text,textsize)

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.r + p2.r:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.a
        angle2 = 2*tangent - p2.a
        speed1 = p2.v
        speed2 = p1.v

        (p1.a, p1.v) = (angle1, speed1)
        (p2.a, p2.v) = (angle2, speed2)
        
        
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)
        
class gameboard:
    
    def __init__(self):
        self.balls = []
        self.score = 0
        for n in range(15):
            self.add_ball()
        
    def update(self, dt):
        if len(self.balls) < 15:
            self.add_ball()
        
        for ball in self.balls:
            ball.move(dt)
            self.check_coll()
    
    def gameover(self):
        for ball in self.balls:
            if ball.check_ball_point() == True:
                return True
        return False
    
    def check_coll(self):
        for ball in self.balls:
            ball.wall_coll()    
        for i, ball1 in enumerate(self.balls):
            for ball2 in self.balls[i+1:]:
                collide(ball1, ball2)
                    
    def reset_board(self):
        self.balls = []
        self.score = 0
        
    def add_ball(self):
        x = random.randint(200,screen_width-200)
        y = random.randint(200,screen_height-200)
        r = 25*random.randint(2,7)

        for ball1 in self.balls:
            dx = x - ball1.x
            dy = y - ball1.y
            dist = math.hypot(dx, dy)
            if dist < r + ball1.r + 5:
                break
        else:
            self.balls.append(ball(x, y, r, random.randint(0,360)*math.pi/180, 10))      

    def burst(self, mouse_x, mouse_y):
        for i, ball1 in enumerate(self.balls):
            if mouse_x < ball1.x + ball1.r and mouse_x > ball1.x - ball1.r and mouse_y < ball1.y + ball1.r and mouse_y > ball1.y - ball1.r:
                self.balls.pop(i)
                
                if ball1.r > 50:
                    r = ball1.r/(1+2**0.5)
                    x = [ball1.x - r, ball1.x + r]
                    y = [ball1.y - r, ball1.y + r]
                    for i in x:
                        for j in y:
                            self.balls.append(ball(i, j, r, random.randint(0,360)*math.pi/180, 10))
                    break
                else:
                  self.score += 1
    
    def render(self, screen, gameover):
        
        if not gameover:
            screen.fill(BLACK)
            for ball in self.balls:
                ball.render(screen)  
                
            font = pygame.font.SysFont(None, 40)
            text = font.render('Score: ' + str(self.score), True, WHITE)
            screen.blit(text,(10,10))        
        
        else:
            font = pygame.font.SysFont(None, 80)
            text = font.render('Game Over', True, WHITE)
            screen.blit(text,(screen_width/4, screen_height/2))  

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

board = gameboard()


crashed = False
clock = pygame.time.Clock()
reset = 0

while not crashed:
    dt = clock.tick(60)
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            crashed = True   
            
        if pygame.mouse.get_pressed()[0] == 1 and reset == 0:
            reset = 1
            board.burst(mouse_x, mouse_y)
            
        if pygame.mouse.get_pressed()[0] == 0:
            reset = 0
        
    gameover = board.gameover()
    board.update(dt)
    board.render(screen, gameover)
    pygame.display.update()
    
pygame.quit()
