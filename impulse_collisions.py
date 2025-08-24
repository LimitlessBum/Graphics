from dataclasses import dataclass
import pygame
import math
import random

pygame.init()
ball_list = []
anchor_list = []
ball_color = [209, 178, 220]
anchor_color = [190, 186, 134]
LENGTH, HEIGHT, FPS = 800, 800, 60
font = pygame.font.SysFont(None, 25)
surface = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption('PROJECT 7')
clock = pygame.time.Clock()

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
    mass: float

    @staticmethod
    def from_radius(x, y, vx, vy, ax, ay, radius, g):
        mass = 0.6 * math.pi * radius**2
        return Ball(x, y, vx, vy, ax, ay, radius, g, mass)
    
    def acceleration(self):
        return Ball(
            x = self.x,
            y = self.y,
            vx = self.vx + self.ax,
            vy = self.vy + self.ay,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g,
            mass = self.mass
        )
    
    def position(self):
        return Ball(
            x = self.x + self.vx,
            y = self.y + self.vy,
            vx = self.vx,
            vy = self.vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g,
            mass = self.mass
        )
    
    def draw(self, surface):
        pygame.draw.circle(surface, ball_color, (int(self.x), int(self.y)), self.radius)

    def wall_collision(self):
        new_vx = self.vx
        new_vy = self.vy
        new_y = self.y
        new_x = self.x
        if self.x + self.radius >= LENGTH:
            new_x = LENGTH - self.radius
            new_vx = self.vx * -1
        if self.x - self.radius <= 0:
            new_x = self.radius
            new_vx = self.vx * -1
        if self.y - self.radius <= 0:
            new_y = self.radius
            new_vy = self.vy * -1
        if self.y + self.radius >= HEIGHT:
            new_y = HEIGHT - self.radius
            new_vy = self.vy * self.g
        return Ball(
            x = new_x,
            y = new_y,
            vx = new_vx,
            vy = new_vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g,
            mass = self.mass
        )

    def ball_collision_overlap(self, other):
        e = 1
        m1 = self.mass
        m2 = other.mass
        dx = self.x - other.x
        dy = self.y - other.y
        d = math.hypot(dx, dy)
        if d == 0:
            d = 1e-8
        if d > self.radius + other.radius:
            return self, other
        nx = dx/d
        ny = dy/d
        rvx = self.vx - other.vx
        rvy = self.vy - other.vy
        rv_dot = rvx * nx + rvy * ny
        if rv_dot > 0:
            return self, other
        overlap = 0.5 * (self.radius + other.radius - d)
        j = ((1 + e) * -rv_dot)/((1/m1) + (1/m2))
        impulse_x = j * nx
        impulse_y = j * ny
        new_x1 = self.x + (nx * overlap)
        new_y1 = self.y + (ny * overlap)
        new_x2 = other.x - (nx * overlap)
        new_y2 = other.y - (ny * overlap)
        new_vx1 = (impulse_x/m1) + self.vx
        new_vy1 = (impulse_y/m1) + self.vy
        new_vx2 = -(impulse_x/m2) + other.vx
        new_vy2 = -(impulse_y/m2) + other.vy
        ball_1 = Ball(
            x = new_x1,
            y = new_y1,
            vx = new_vx1,
            vy = new_vy1,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g,
            mass = self.mass
        )
        ball_2 = Ball(
            x = new_x2,
            y = new_y2,
            vx = new_vx2,
            vy = new_vy2,
            ax = other.ax,
            ay = other.ay,
            radius = other.radius,
            g = other.g,
            mass = other.mass
        )
        return ball_1, ball_2
    
    def visual_velocity(self, surface):
        width = 6
        dx = self.vx
        dy = self.vy
        d = math.hypot(dx, dy)
        if d == 0:
            return
        nx = dx/d
        ny = dy/d
        S = d * 2
        new_x = self.x + (nx * S)
        new_y = self.y + (ny * S)
        velocity = f"{d:.2f}"
        pygame.draw.line(surface, (100, 120, 110), (int(self.x), int(self.y)), (new_x, new_y), width)
        text_surf = font.render(velocity, True, (255, 255, 255))
        text_shape = text_surf.get_rect(center = (new_x - 15, new_y - 15))
        surface.blit(text_surf, text_shape)

@dataclass(frozen = True)
class Anchor:
    x: float
    y: float
    vx: float
    vy: float
    ax: float
    ay: float
    radius: int
    g: float
    mass: float

    @staticmethod
    def from_anchor_radius(x, y, vx, vy, ax, ay, radius, g):
        mass = math.inf
        return Anchor(x, y, vx, vy, ax, ay, radius, g, mass)
    
    def anchor_position(self):
        return Anchor(
            x = self.x, 
            y = self.y,
            vx = self.vx,
            vy = self.vy,
            ax = self.ax,
            ay = self.ay,
            radius = self.radius,
            g = self.g,
            mass = self.mass
        )
    
    def anchor_collide(self, other):
        m2 = other.mass
        e = 1
        dx = other.x - self.x
        dy = other.y - self.y
        d = math.hypot(dx, dy)
        if d == 0:
            d = 1e-8
        if d > self.radius + other.radius:
            return self, other
        overlap = 0.5 * (self.radius + other.radius - d)
        nx = dx/d
        ny = dy/d
        rvx = other.vx
        rvy = other.vy
        rv_dot = rvx * nx + rvy * ny
        if rv_dot > 0:
            return self, other
        j = ((1 + e) * -rv_dot) * m2
        impulse_x = j * nx
        impulse_y = j * ny
        new_x = other.x + (nx * overlap)
        new_y = other.y + (ny * overlap)
        new_vx = (impulse_x/m2) + other.vx
        new_vy = (impulse_y/m2) + other.vy
        new_ball = Ball(
            x = new_x,
            y = new_y,
            vx = new_vx,
            vy = new_vy,
            ax = other.ax,
            ay = other.ay,
            radius = other.radius,
            g = other.g,
            mass = other.mass
        )
        return self, new_ball


    
    def draw(self, surface):
        pygame.draw.circle(surface, anchor_color, (int(self.x), int(self.y)), self.radius)


for _ in range(7):
    x_pos = random.randint(100, 700)
    y_pos = random.randint(25, 200)
    r = random.randint(12, 18)
    z = Ball.from_radius(x = x_pos, y = y_pos, vx = 2, vy = 3, ax = 0, ay = 1.1, radius = r, g = -0.98)
    ball_list.append(z)

for _ in range(1):
    anchor_x = random.randint(400, 410)
    anchor_y = random.randint(390, 410)
    w = Anchor.from_anchor_radius(x = anchor_x, y = anchor_y, vx = 0, vy = 0, ax = 0, ay = 0, radius = 23, g = -0.98)
    anchor_list.append(w)

def kinetic(P):
    vx = P.vx
    vy = P.vy
    m = P.mass
    v_sq = vx**2 + vy**2
    return 0.5 * m * v_sq

def total():
    return sum(kinetic(P) for P in ball_list)

running = True
while running:
    clock.tick(FPS)
    surface.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for i in range(len(ball_list)):
        for j in range(i + 1, len(ball_list)):
            EK_BEFORE = total()
            print(f"EK BEFORE = {EK_BEFORE:.2f}")
            ball_list[i], ball_list[j] = ball_list[i].ball_collision_overlap(ball_list[j])
            EK_AFTER = total()
            print(f"EK AFTER = {EK_AFTER:.2f}")
            delta = EK_AFTER - EK_BEFORE
            print(f"CHANGE = {delta:.2f}")

        for anchor in anchor_list:
            anchor, ball_list[i] = anchor.anchor_collide(ball_list[i])


    for a in range(len(ball_list)):
        b = ball_list[a]
        b = b.acceleration()
        b = b.position()
        b = b.wall_collision()
        b.draw(surface)
        b.visual_velocity(surface)
        ball_list[a] = b 

    for c in anchor_list:
        c = c.anchor_position()
        c.draw(surface)

    
    pygame.display.flip()
pygame.quit()
