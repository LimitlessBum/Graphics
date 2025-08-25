# import libraries
from dataclasses import dataclass
import math
import random
import pygame
 
# length of screen
l = 1000
# height of screen
h = 500
# frames per second
fps = 60
# screen color
black = (0, 0, 0)
# ball color
ball_color = (78, 65, 77)
# boolean start
run = True

#setup
pygame.init()
screen = pygame.display.set_mode((l,h))
pygame.display.set_caption('Mouse')
clock = pygame.time.Clock()

# ball class
@dataclass(frozen = True)
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    ax: float
    ay: float
    radius: int
    g: float

    # compute acceleration of object
    def acceleration(self):
        return Ball(
            x = self.x,
            y = self.y,
            vx = self.vx + self.ax,
            vy = self.vy + self.ay,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g
        )
    
    # compute position of object
    def position(self):
        return Ball(
            x = self.x + self.vx,
            y = self.y + self.vy,
            vx = self.vx,
            vy = self.vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g
        )
    
    # account for wall collisions
    def wall(self):
        wall_x = self.x
        wall_y = self.y
        wall_vx = self.vx
        wall_vy = self.vy
        if self.x - self.radius <= 0:
            wall_x = self.radius
            wall_vx = self.vx * -1
        if self.x + self.radius >= l:
            wall_x = l - self.radius
            wall_vx = self.vx * -1
        if self.y - self.radius <= 0:
            wall_y = self.radius
            wall_vy = self.vy * -1
        if self.y + self.radius >= h:
            wall_y = h - self.radius
            wall_vy = self.vy * self.g
        return Ball(
            x = wall_x,
            y = wall_y,
            vx = wall_vx,
            vy = wall_vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g
        )
    
    # draw ball
    def ball_draw(self, screen):
        pygame.draw.circle(screen, ball_color, (int(self.x), int(self.y)), self.radius)

    # compute speed in mouse direction if mouse is detected
    def move_to_mouse(self):
        point_x, point_y = pygame.mouse.get_pos()
        dx = point_x - self.x
        dy = point_y - self.y
        linear_factor = 0.1
        speed = 40
        d = math.hypot(dx, dy)
        if d != 0:

            # compute normal vectors 
            nx = dx/d
            ny = dy/d
            return Ball(
                x = self.x + (point_x - self.x) * linear_factor,
                y = self.y + (point_y - self.y) * linear_factor,
                vx = linear_factor * speed * nx,
                vy = linear_factor * speed * ny,
                ax = 0,
                ay = 0,
                radius = self.radius,
                g = self.g
            )
        else:
            return self
        
# basic attributes for object
val = random.randint(14, 20)
r = random.randint(15, 18)
if val - r <= 0:
    val = r
X = Ball(x = val, y = val, vx = 2, vy = 3, ax = 0, ay = 0.7, radius = r, g = -0.98)

# main
while run:
    clock.tick(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # if mouse is detected inside screen
    if pygame.mouse.get_focused():
        X = X.move_to_mouse()
    # if mouse not detected
    else:
        X = X.acceleration()
        X = X.position()
        X = X.wall()
    X.ball_draw(screen)
    

    pygame.display.flip()
pygame.quit()