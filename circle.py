from functools import cache
import pygame
import math
import time

pygame.init()
pygame.display.set_caption("원운동 가상 실험")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
BLACK = (0, 0 ,0)
FPS = 1000
size = (1200, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)
def right_std_pos(pos):
    return [pos[0] + 900, pos[1] + size[1]//2]
def left_std_pos(pos):
    return [pos[0] + 300, pos[1] + size[1]//2]

circle_r = 10
mass = 0.02         # 구의 질량
gravity = 9.8       # 중력 가속도
orbit_r = 0.3       # 끈의 길이
angular_velocity = math.radians(360*2)   # 각속도(rad/s)
spin_theta = 0
height_theta = math.atan((mass*gravity)/(mass*math.pow(angular_velocity, 2)*orbit_r)) # 직각 - (막대와 끈 사이의 각도)
rate = 250 / orbit_r    # 실제 길이와 픽셀 수 사이의 비율

side_x = orbit_r*math.cos(height_theta)*rate + circle_r*math.cos(height_theta)
side_y = orbit_r*math.sin(height_theta)*rate + circle_r*math.sin(height_theta)

start_t = time.time()

while not done:
    clock.tick(FPS)
    screen.fill(BLACK)

    try: # 일정한 속도로 프로그램 반복 실행
        df = 1 / clock.get_fps()   # 프레임당 차지하는 시간(s)
    except:
        df = 1 / FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    spin_theta += math.degrees(angular_velocity) * df
    if spin_theta >= 360:
        spin_theta -= 360
        start_t = time.time()
    
    up_circle_pos = (side_x*math.cos(math.radians(spin_theta)), side_x*math.sin(math.radians(spin_theta))) # 구의 위치(우)
    pygame.draw.circle(screen, WHITE, right_std_pos(up_circle_pos), circle_r)
    pygame.draw.line(screen, YELLOW, right_std_pos([0, 0]), right_std_pos(up_circle_pos), 2)
    pygame.draw.circle(screen, GRAY, right_std_pos([0, 0]), 3)

    side_circle_pos = (side_x*math.cos(math.radians(spin_theta)), side_y) # 구의 위치(좌)
    if spin_theta <= 180:
        pygame.draw.line(screen, GRAY, left_std_pos([0, 0]), left_std_pos([0, 250]), 6)
        pygame.draw.line(screen, YELLOW, left_std_pos([0, 0]), left_std_pos(side_circle_pos), 2)
        pygame.draw.circle(screen, WHITE, left_std_pos(side_circle_pos), circle_r)
    else:
        pygame.draw.circle(screen, WHITE, left_std_pos(side_circle_pos), circle_r)
        pygame.draw.line(screen, YELLOW, left_std_pos([0, 0]), left_std_pos(side_circle_pos), 2)
        pygame.draw.line(screen, GRAY, left_std_pos([0, 0]), left_std_pos([0, 250]), 6)

    height_theta_txt = font(30).render(f"tri_degree : {90 - math.degrees(height_theta):.2f}", True, WHITE) # 축과 끈 사이 각도
    screen.blit(height_theta_txt, (0, 0))

    pygame.display.update()

pygame.quit()