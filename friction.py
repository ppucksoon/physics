from functools import cache
import pygame
import math
import time

pygame.init()
pygame.display.set_caption("마찰력 가상 실험")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0 ,0)
FPS = 1000
size = (800, 800)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

board = 0.564       # 빗면의 길이
tri_degree = 20     # 빗면의 각도(˚)
tri_theta = math.radians(tri_degree)    # 빗면의 각도(rad)
tri_pos = [[100, 750], [700, 750], [0, 0]]
tri_pos[2] = [tri_pos[1][0], tri_pos[1][1] - math.tan(tri_theta)*(tri_pos[1][0]-tri_pos[0][0])]
mass = 0.25     # 물체의 질량
gravity = 9.8   # 중력 가속도
mu_s = math.tan(math.radians(15))   # 정시 마찰계수
mu_k = 0.4/(0.25*9.8)               # 운동 마찰계수
df = 1 / FPS    # 프레임당 차지하는 시간(s)

start_t = time.time()
stop_t = time.time()

def reset():
    global acceleration, stop, no_move, velocity, object_delta_pos, \
        object_pos, tri_degree, tri_theta, tri_pos, gravity, mu_s, rate
    stop = False
    no_move = False
    tri_theta = math.radians(tri_degree)
    acceleration = gravity*(math.sin(tri_theta) - mu_s*math.cos(tri_theta))
    if acceleration <= 0:
        acceleration = 0
        stop = True
        no_move = True
    velocity = acceleration*df
    object_delta_pos = 0
    object_pos = [0, 0]
    tri_pos[2] = [tri_pos[1][0], tri_pos[1][1] - math.tan(tri_theta)*(tri_pos[1][0]-tri_pos[0][0])]
    rate = math.sqrt(math.pow(tri_pos[0][0]-tri_pos[1][0], 2) + math.pow(tri_pos[1][1]-tri_pos[2][1], 2))/board
    # 실제 길이와 픽셀 수 사이의 비율

reset()

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    try:
        df = 1 / clock.get_fps()
    except:
        df = 1 / FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                tri_degree += 10
            if event.key == pygame.K_w:
                tri_degree += 1
            if event.key == pygame.K_a:
                tri_degree -= 10
            if event.key == pygame.K_s:
                tri_degree -= 1
            if tri_degree <= 0:
                tri_degree = 0

            reset()
            start_t = time.time()
    
    if not stop:
        acceleration = gravity*(math.sin(tri_theta) - mu_k*math.cos(tri_theta))
        velocity += acceleration*df
        object_delta_pos += velocity*df
        object_pos[0] += velocity*df*math.cos(tri_theta)*rate
        object_pos[1] += velocity*df*math.sin(tri_theta)*rate

    if object_delta_pos >= board and not stop:
        stop = True
        stop_t = time.time()
        print(f'소요 시간 : {time.time() - start_t} 초')
    
    if no_move:
        pass
    elif stop and time.time() - stop_t >= 1:
        object_delta_pos = 0
        object_pos = [0, 0]
        start_t = time.time()
        stop = False
        reset()

    pygame.draw.circle(screen, WHITE, (tri_pos[2][0] - object_pos[0], tri_pos[2][1] + object_pos[1]-15), 15)
    pygame.draw.polygon(screen, GRAY, tri_pos)

    tri_degree_txt = font(30).render(f"tri_degree : {tri_degree:.2f}", True, WHITE)
    screen.blit(tri_degree_txt, (0, 0))

    pygame.display.update()

pygame.quit()