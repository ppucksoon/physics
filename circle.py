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

def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)
def up_std_pos(pos):
    return [pos[0] + 900, pos[1] + size[1]//2]
def side_std_pos(pos):
    return [pos[0] + 300, pos[1] + size[1]//2]

circle_r = 10       # 구의 반지름
mass = 0.2          # 구의 질량
gravity = 98*100000 # 중력 가속도
orbit_r = 290       # 끈의 길이
theta = 0
tangent_velocity = orbit_r*360  # 접선(순간) 속도 --> 끈의 길이 * 각속도
angular_velocity = tangent_velocity / orbit_r   # 각속도
side_theta = math.atan((mass*gravity)/(mass*math.pow(tangent_velocity, 2)/orbit_r))
side_x = (orbit_r+circle_r)*math.cos(side_theta)
side_y = (orbit_r+circle_r)*math.sin(side_theta)
start_t = time.time()

while not done:
    df = clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    theta += angular_velocity * df / 1000
    if theta >= 360:
        theta -= 360
        print(f"구의 주기 : {time.time() - start_t} 초")
        start_t = time.time()
    
    circle_pos = (side_x*math.cos(math.radians(theta)), side_x*math.sin(math.radians(theta)))
    pygame.draw.circle(screen, WHITE, up_std_pos(circle_pos), circle_r)
    pygame.draw.line(screen, YELLOW, up_std_pos([0, 0]), up_std_pos(circle_pos), 2)
    pygame.draw.circle(screen, GRAY, up_std_pos([0, 0]), 3)

    circle_pos = (side_x*math.cos(math.radians(theta)), side_y)
    if theta <= 180:
        pygame.draw.line(screen, GRAY, side_std_pos([0, 0]), side_std_pos([0, 250]), 6)
        pygame.draw.line(screen, YELLOW, side_std_pos([0, 0]), side_std_pos(circle_pos), 2)
        pygame.draw.circle(screen, WHITE, side_std_pos(circle_pos), circle_r)
    else:
        pygame.draw.circle(screen, WHITE, side_std_pos(circle_pos), circle_r)
        pygame.draw.line(screen, YELLOW, side_std_pos([0, 0]), side_std_pos(circle_pos), 2)
        pygame.draw.line(screen, GRAY, side_std_pos([0, 0]), side_std_pos([0, 250]), 6)

    pygame.display.update()

pygame.quit()