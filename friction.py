import pygame
import math
import time

pygame.init()
pygame.display.set_caption("마찰력 가상 실험")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0 ,0)
FPS = 60
size = (800, 800)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

box_length = (50, 30)
box = pygame.image.load('./img/box.png')
box = pygame.transform.scale(box, box_length)

def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

def blitRotate(image, pos, originPos, angle): 
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]] 
    box_rotate = [p.rotate(angle) for p in box] 
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1]) 
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1]) 
 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1]) 
    pivot_rotate = pivot.rotate(angle) 
    pivot_move   = pivot_rotate - pivot 
 
    origin = ((pos[0] - originPos[0] + min_box[0] - pivot_move[0]), (pos[1] - originPos[1] - max_box[1] + pivot_move[1])) 
 
    rotated_image = pygame.transform.rotate(image, angle) 
    return (rotated_image, origin)

def getRotate(cri_pos, pos):
    deltaX = pos[0] - cri_pos[0]
    deltaY = pos[1] - cri_pos[1]
    value = math.degrees(math.atan2(deltaX, deltaY)) -90
    if value < 0:
        value += 360
    return value

tri_pos = ((100, 700), (700, 700), (700, 200))
mass = 0.2
mu_s = 0.74
mu_k = 0.57
gravity = 9.8
r = getRotate(tri_pos[0], tri_pos[2])
diagonal_length = math.sqrt(math.pow(box_length[0], 2) + math.pow(box_length[1], 2))
diagonal_theta = math.atan(box_length[1] / box_length[0])
tri_theta = math.atan((tri_pos[1][1] - tri_pos[2][1])/(tri_pos[1][0] - tri_pos[0][0]))
box_rb_pos = [tri_pos[2][0], tri_pos[2][1]]
stop = False
acceleration = gravity*(math.sin(tri_theta) - mu_s*math.cos(tri_theta))
if acceleration <= 0:
    acceleration = 0
velocity = acceleration

start_t = time.time()

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if time.time() - start_t >= 0.01 and not stop:
        start_t = time.time()
        if acceleration > 0:
            acceleration = gravity*(math.sin(tri_theta) - mu_k*math.cos(tri_theta))
        velocity += acceleration*0.01
        box_rb_pos[0] -= velocity*math.cos(tri_theta)
        box_rb_pos[1] += velocity*math.sin(tri_theta)
    
    if box_rb_pos[0] - box_length[0]*math.cos(tri_theta) <= tri_pos[0][0]:
        stop = True

    if stop and time.time() - start_t >= 1.5:
        stop = False
        box_rb_pos = [tri_pos[2][0], tri_pos[2][1]]
        acceleration = gravity*(math.sin(tri_theta) - mu_s*math.cos(tri_theta))
        if acceleration <= 0:
            acceleration = 0
        velocity = acceleration

    box_pos = [(-diagonal_length/2*math.cos(tri_theta - diagonal_theta) + box_rb_pos[0]), \
        (diagonal_length/2*math.sin(tri_theta - diagonal_theta) + box_rb_pos[1])]
    rotate_box = blitRotate(box, box_pos, (box_length[0]//2, box_length[1]//2), r)
    screen.blit(rotate_box[0], rotate_box[1])
    pygame.draw.polygon(screen, GRAY, tri_pos)

    pygame.display.update()

pygame.quit()