# import libraries
from dataclasses import dataclass
import math
import pygame
import random

# Arrays
list_1 = []   # ball list
list_2 = []   # trail array for store previous x and y positions of ball
list_3 = [0, 0, 0]   # screen color
list_4 = [85, 73, 142]   # ball color

# Variables 
l = 900
w = 500
fps = 60
density = 0.6
max_trail_length = 15   # max length before trail starts fading out 
run = True

# Setup
pygame.init()
screen = pygame.display.set_mode((l, w))
pygame.display.set_caption('Bouncing Ball')
clock = pygame.time.Clock()

# Ball class
@dataclass(frozen = True)
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    ax: float
    ay: float
    radius: int
    gravity: float
    mass: float

    # compute mass from radius
    @staticmethod
    def from_radius(x, y, vx, vy, ax, ay, radius, gravity):
        mass = density * math.pi * radius**2
        return Ball(x, y, vx, vy, ax, ay, radius, gravity, mass)
    
    # compute position
    def position(self):
        return Ball(
            x = self.x + self.vx,
            y = self.y + self.vy,
            vx = self.vx,
            vy = self.vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            gravity = self.gravity,
            mass = self.mass
        )
    
    # compute acceleration
    def acceleration(self):
        return Ball(
            x = self.x,
            y = self.y,
            vx = self.vx + self.ax,
            vy = self.vy + self.ay,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            gravity = self.gravity,
            mass = self.mass
        )
    
    # draw function
    def draw(self, screen):
        pygame.draw.circle(screen, list_4, (int(self.x), int(self.y)), self.radius)
    
    # ball rebounds off window screen
    def wall(self):
        wall_x = self.x
        wall_y = self.y
        wall_vx = self.vx
        wall_vy = self.vy
        if self.x - self.radius <= 0:
            wall_x = self.radius 
            wall_vx = self.vx * -1 
        if self.y - self.radius <= 0:
            wall_y = self.radius 
            wall_vy = self.vy * -1
        if self.x + self.radius >= l:
            wall_x = l - self.radius
            wall_vx = self.vx * -1 
        if self.y + self.radius >= w:
            wall_y = w - self.radius
            wall_vy = self.vy * self.gravity
        return Ball(
            x = wall_x,
            y = wall_y,
            vx = wall_vx,
            vy = wall_vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            gravity = self.gravity,
            mass = self.mass
        )


# helper to generate ball basic attributes
for _ in range(1):
    y_val = random.randint(21, 100)   # y-position of centre of ball
    r = random.randint(12, 16)   # radius value of ball
    x_val = random.randint(21, 400)   # x-position of centre of ball
    if x_val - r <= 0:   # check if ball (or part of ball) is outside screen bounds
        x_val = r   # centre x_position is clamped to screen r units from the left
    X = list_1.append(Ball.from_radius(x = x_val, y = y_val, vx = 2, vy = 3, ax = 0, ay = 0.5, radius = r, gravity = -0.98))



# Main
while run:
    clock.tick(fps)
    screen.fill(list_3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for balls in range(len(list_1)):
        a = list_1[balls]
        a = a.acceleration()
        a = a.position()
        list_2.append((a.x, a.y))
        if len(list_2) > max_trail_length:   # when number of positions exceed max length allowed, first element
            list_2.pop(0)                    # of array is removed as newer positions are filled in

        a = a.wall()
        for i, pos in enumerate(list_2):   # i is index of current position in list_2, pos is actual (x,y) coordinates
            alpha = (255 * (1 - i/max_trail_length))   # alpha makes older points fade out over time
            trail_color = (205, 245, 155, int(alpha))  # RGB colors for trail 
            size = (6, 6)   # size dictates how big each circle surface is 
            surf = pygame.Surface(size, pygame.SRCALPHA)   # dot draw on it's own mini-surface with transparency via srcalpha
            pygame.draw.circle(surf, trail_color, (size[0]//2, size[1]//2), size[0]//2)   # trail marks (circles) are centered on the ball object
            screen.blit(surf, (pos[0] - size[0]//2, pos[1] -  size[1]//2))   # places the trail onto the main surface
        a.draw(screen)
        list_1[balls] = a

    pygame.display.flip()
pygame.quit()