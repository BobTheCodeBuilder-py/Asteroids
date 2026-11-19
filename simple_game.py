import pygame as pg
import math
import random

pg.init()

size_coeficient = 100
size = (16*size_coeficient, 10*size_coeficient)
version = "pre-alpha v0.1"
caption = "Asteroid"+" "+version
window = pg.display.set_mode(size)
overlay = pg.Surface(size, pg.SRCALPHA)
pg.display.set_caption(caption)

BLACK = (27, 26, 54)
LBLACK = (56, 44, 94)
LBLUE = (90, 71, 150)
CYAN = (102, 80, 171)
GREEN = (204, 172, 27)
ORANGE = (204, 139, 27)
BGREEN = (50, 168, 139)
LBGREEN = (16, 227, 175) 
PURPLE = (125, 41, 227)
WHITE = (255, 255, 255)
ASTEROID_COLOR = (81, 94, 112)
loop = True

clock = pg.time.Clock()
FPS = 60

x = size[0]//2
y = size[1]//2
normal = 0
speedx = 0
speedy = 0
speed_coeficient = 1
friction = 0.9
angle = 0

pause = 0
space = 0

font1 = pg.font.SysFont("Arial", 50)
font2 = pg.font.SysFont("Arial", 20)

projectile_positions = []
projectile_speeds = []
asteroid_positions = []
asteroid_speeds = []

def draw_player(x, y, radius):
    pg.draw.circle(window, GREEN, (x, y), radius//2, 0)
    if pause == 0:
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - x
        dy = mouse_y - y
        angle = math.atan2(dy, dx) - math.pi / 2
        p1 = rotate_around_pivot((x-2*radius, y-radius), (x, y), angle)
        p2 = rotate_around_pivot((x+2*radius, y-radius), (x, y), angle)
        p3 = rotate_around_pivot((x, y+radius*3), (x, y), angle)
        triangle1_points = [p1, p2, p3]
        pg.draw.polygon(window, ORANGE, triangle1_points, 0)
        p4 = rotate_around_pivot((x-radius, y-2*radius), (x, y), angle)
        p5 = rotate_around_pivot((x+radius, y-2*radius), (x, y), angle)
        p6 = rotate_around_pivot((x, y+radius*2), (x, y), angle)
        triangle1_points = [p4, p5, p6]
        pg.draw.polygon(window, PURPLE, triangle1_points, 0)
        return angle

def draw_keys(x, y, keyx, keyy):
    if keyy == -1:
        pg.draw.rect(window, LBLUE, (x, y, 30, 30), 0, border_radius = 10)
    else:
        pg.draw.rect(window, LBLACK, (x, y, 30, 30), 0, border_radius = 10)
    if keyy == 1:
        pg.draw.rect(window, LBLUE, (x, y+32, 30, 30), 0, border_radius = 10)
    else:
        pg.draw.rect(window, LBLACK, (x, y+32, 30, 30), 0, border_radius = 10)
    if keyx == 1:
        pg.draw.rect(window, LBLUE, (x+32, y+32, 30, 30), 0, border_radius = 10)
    else:
        pg.draw.rect(window, LBLACK, (x+32, y+32, 30, 30), 0, border_radius = 10)
    if keyx == -1:
        pg.draw.rect(window, LBLUE, (x-32, y+32, 30, 30), 0, border_radius = 10)
    else:
        pg.draw.rect(window, LBLACK, (x-32, y+32, 30, 30), 0, border_radius = 10)
    pg.draw.polygon(window, CYAN, [(x+15, y+5), (x+5, y+23), (x+25, y+23)], 5)
    pg.draw.circle(window, CYAN, (x+15, y+47), 12, 5)
    pg.draw.line(window, CYAN, (x-25, y+47), (x-10, y+47), 5)
    pg.draw.line(window, CYAN, (x+55, y+47), (x+40, y+47), 5)

def draw_space(x, y, space):
    if space == 1:
        pg.draw.rect(window, LBLUE, (x, y, 90, 30), 0, border_radius = 10)
    else:
        pg.draw.rect(window, LBLACK, (x, y, 90, 30), 0, border_radius = 10)
    pg.draw.line(window, CYAN, (x+10, y+15), (x+80, y+15), 5)

def keys_clicked(x, y):
    global keyx, keyy
    mouse_pos = pg.mouse.get_pos()
    mouse_buttons = pg.mouse.get_pressed()
    rect1 = pg.Rect(x, y, 30, 30)
    rect2 = pg.Rect(x, y+32, 30, 30)
    rect3 = pg.Rect(x+32, y+32, 30, 30)
    rect4 = pg.Rect(x-32, y+32, 30, 30)
    if mouse_buttons[0]:
        if rect1.collidepoint(mouse_pos):
            keyy = -1
        elif rect2.collidepoint(mouse_pos):
            keyy = 1
        elif rect3.collidepoint(mouse_pos):
            keyx = 1
        elif rect4.collidepoint(mouse_pos):
            keyx = -1

def space_clicked(x, y):
    global space
    mouse_pos = pg.mouse.get_pos()
    mouse_buttons = pg.mouse.get_pressed()
    rect1 = pg.Rect(x, y, 90, 30)
    if mouse_buttons[0] and rect1.collidepoint(mouse_pos):
        space = 1

def draw_pause_button(x, y, pause):
    if pause == 1:
        pg.draw.rect(window, LBLUE, (x, y, 40, 40), 0, border_radius=10)
        pg.draw.line(window, CYAN, (x+10, y+10), (x+30, y+30), 5)
        pg.draw.line(window, CYAN, (x+10, y+30), (x+30, y+10), 5)
    else:
        pg.draw.rect(window, LBLACK, (x, y, 40, 40), 0, border_radius=10)
        pg.draw.circle(window, CYAN, (x+20, y+20), 15, 5)

def pause_button_clicked(x, y, event):
    global pause
    mouse_pos = pg.mouse.get_pos()
    rect1 = pg.Rect(x, y, 40, 40)
    if rect1.collidepoint(mouse_pos):
        pause = 1-pause
        
def check_out_of_bounds(x, y, radius):
    global speedx, speedy
    if x-radius < 0:
        x=radius
        speedx = 0
    elif x+radius > size[0]:
        x=size[0]-radius
        speedx = 0
    if y-radius < 0:
        y=radius
        speedy = 0
    elif y+radius > size[1]:
        y = size[1]-radius
        speedy = 0
    return(x, y)

def draw_overlay(transparency):
    overlay.fill((255, 255, 255, transparency))
    window.blit(overlay, (0, 0))

def draw_text(text, pos, color, font):
    if font == 1:
        txt = font1.render(str(text), True, color)
    elif font == 2:
        txt = font2.render(str(text), True, color)
    window.blit(txt, pos)

def rotate_around_pivot(point, pivot, angle):
    """Rotates a point around a specific pivot point by an angle in radians."""
    px, py = pivot
    x, y = point
    
    temp_x = x - px
    temp_y = y - py
    
    rot_x = temp_x * math.cos(angle) - temp_y * math.sin(angle)
    rot_y = temp_x * math.sin(angle) + temp_y * math.cos(angle)
    
    final_x = rot_x + px
    final_y = rot_y + py
    return final_x, final_y

def spawn_projectile(x, y, velocity, angle):
    angle += math.pi / 2
    global projectile_positions, projectile_speeds
    projectile_positions.append((x, y))
    velocity_x = velocity * math.cos(angle)
    velocity_y = velocity * math.sin(angle)
    projectile_speeds.append((velocity_x+speedx, velocity_y+speedy))

def draw_projectiles(color):
    global projectile_positions, projectile_speeds
    if len(projectile_positions) > 0:
        for i in projectile_positions:
            pg.draw.circle(window, color, i, 5, 0)

def tick_projectiles():
    global projectile_positions, projectile_speeds, loop
    if len(projectile_positions) != len(projectile_speeds):
        loop = False
    tmpls = []
    for i in range(len(projectile_positions)):
        pos = projectile_positions[i]
        x = pos[0]
        y = pos[1]
        v = projectile_speeds[i]
        vx = v[0]
        vy = v[1]
        if (x < 0 or x > size[0]) or (y < 0 or y > size[1]):
            tmpls.insert(0, i)

        x += vx
        y += vy
        projectile_positions[i] = (x, y)
    if len(tmpls) > 0:
        for i in tmpls:
            if i <= len(projectile_positions):
                projectile_positions.pop(i)
                projectile_speeds.pop(i)

def draw_cursor(rad):
    mouse_x, mouse_y = pg.mouse.get_pos()
    pg.draw.circle(window, WHITE, (mouse_x, mouse_y), rad, width=3)
    pg.draw.line(window, WHITE, (mouse_x, mouse_y+rad), (mouse_x, mouse_y+rad*2), width=3)
    pg.draw.line(window, WHITE, (mouse_x, mouse_y-rad), (mouse_x, mouse_y-rad*2), width=3)
    pg.draw.line(window, WHITE, (mouse_x+rad, mouse_y), (mouse_x+rad*2, mouse_y), width=3)
    pg.draw.line(window, WHITE, (mouse_x-rad, mouse_y), (mouse_x-rad*2, mouse_y), width=3)

def spawn_asteroid(maxv):
    x = random.randrange(0, size[0])
    y = random.randrange(0, size[1])
    vx = random.randrange(0-maxv, maxv)
    vy = random.randrange(0-maxv, maxv)
    asteroid_positions.append((x, y))
    asteroid_speeds.append((vx, vy))

def draw_asteroids(color):
    if len(asteroid_positions) > 0:
        for i in asteroid_positions:
            pg.draw.circle(window, color, i, 30, 0)

pg.mouse.set_visible(False)
while loop:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
            break
        if event.type == pg.MOUSEBUTTONDOWN:
            pause_button_clicked(size[0]-50, size[1]-50, event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_x:
                spawn_asteroid(3)

    keys = pg.key.get_pressed()
    window.fill(BLACK)
    if pause == 0:
        keyx = ((keys[pg.K_RIGHT] or keys[pg.K_d]) - (keys[pg.K_LEFT] or keys[pg.K_a])) * 1
        keyy = ((keys[pg.K_DOWN] or keys[pg.K_s]) - (keys[pg.K_UP] or keys[pg.K_w])) * 1
        space = keys[pg.K_SPACE] * 1

        keys_clicked(38, size[1]-68)
        space_clicked(size[0]//2-45, size[1]-40)
        tick_projectiles()

        if abs(keyx) + abs(keyy) == 2:
            normal = 1.41
        else:
            normal = 1

        speedx += keyx*speed_coeficient/normal
        speedy += keyy*speed_coeficient/normal

        speedx = speedx * friction
        speedy = speedy * friction

        x += speedx
        y += speedy

        x, y = check_out_of_bounds(x, y, 15)

        if space == 1:
            time += 1
            if time%3 == 0:
                spawn_projectile(int(x), int(y), 10, angle)
        else:
            time = 0

        draw_projectiles(PURPLE)
        draw_asteroids(ASTEROID_COLOR)
        angle = draw_player(x, y, 15)
        draw_keys(38, size[1]-68, keyx, keyy)
        draw_space(size[0]//2-45, size[1]-40, space)
    else:
        draw_overlay(32)
        draw_text("PAUSED -------------------------------", (30, 30), BGREEN, 1)
        draw_text("CREDITS:", (30, 100), LBGREEN, 2)
        draw_text("Albu Dragos Ioan", (50, 130), LBGREEN, 2)
        draw_text("clasa IX -a I", (50, 160), LBGREEN, 2)
        draw_text("VERSION:", (30, 210), LBGREEN, 2)
        draw_text(version, (50, 240), LBGREEN, 2)

    draw_pause_button(size[0]-50, size[1]-50, pause)
    draw_cursor(10)
    pg.display.update()
    clock.tick(FPS)

pg.quit()

print(f"Debug: Remaining Projectiles: {len(projectile_positions)}")