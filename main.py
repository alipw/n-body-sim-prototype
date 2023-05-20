
# Import and initialize the pygame library
import pygame
import numpy as np
import Body
from scipy import constants

SCREENX = 1000.
SCREENY = 1000.
BIG_G = constants.G
FPS = 60
ZOOM_SCALE = 0.1
ZOOM_STEP = 0.02
SCREEN_OFFSET = np.zeros(2)

# from cartesian coordinate with to pygame coordinate system


def to_pygame(coord):
    return np.array([coord[0] + SCREENX / 2, -coord[1] + SCREENY / 2])


def to_cartesian(coord):
    return np.array([coord[0] - SCREENX / 2, -coord[1] + SCREENY / 2])


pygame.init()
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([SCREENX, SCREENY])
pygame.display.set_caption('n-body gravity simulation')


bodies = []

for i in range(50):
    body = Body.Body(massKg=np.random.uniform(10**8, 10**8, 1),
                     velocityMps=np.random.uniform(-0.02, 0.02, 2),
                     color=np.random.randint(0, 255, 3),
                     position=np.random.uniform(-10000, 10000, 2),
                     name="body " + str(i)
                     )
    bodies.append(body)

body = Body.Body(massKg=np.random.uniform(10**11, 10**11, 1),
                    velocityMps=np.random.uniform(-0.02, 0.02, 2),
                    color=np.random.randint(0, 255, 3),
                    position=np.random.uniform(-1, 1, 2),
                    name="body " + str(i)
                    )
bodies.append(body)

# Run until the user asks to quit
font1 = pygame.font.SysFont('notosanstaiviet.ttf', 15)
running = True
drag = False
startdrag = np.array([0., 0.])
follow_body = False
selected_body_to_follow = 2


def loca(position: np.ndarray, offset):
    return to_pygame((position + offset) * ZOOM_SCALE)


while running:

    # Fill the background with white
    screen.fill((0, 0, 0))
    dt = clock.tick(FPS)

    # Did the user click the window close button?

    mousepos = to_cartesian(pygame.mouse.get_pos()) / ZOOM_SCALE
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            startdrag = (mousepos - SCREEN_OFFSET)

        if event.type == pygame.MOUSEBUTTONUP:
            drag = False

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            ZOOM_SCALE -= -event.y * ZOOM_SCALE * ZOOM_STEP

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                follow_body = True

    if drag and not follow_body:
        SCREEN_OFFSET = -(startdrag - mousepos)

    for i in range(len(bodies)):
        ibody = bodies[i]
        for j in range(len(bodies)):
            if i == j:
                continue

            jbody = bodies[j]
            gravity_force = ibody.massKg * jbody.massKg * BIG_G / \
                np.linalg.norm(ibody.position - jbody.position) ** 2

            dv = (jbody.position - ibody.position) * \
                gravity_force / ibody.massKg
            ibody.velocityMps += dv
            ibody.position += ibody.velocityMps * dt

        if i == selected_body_to_follow and follow_body:
            SCREEN_OFFSET = -(ibody.position)
            print(loca(ibody.position, SCREEN_OFFSET))

        name = font1.render(ibody.name, True, (255, 255, 255))
        spd = font1.render(
            "SPD: " + np.array2string(ibody.velocityMps), True, (255, 255, 255))
        pos = font1.render(
            "POS: " + np.array2string(ibody.position), True, (255, 255, 255))
        pygame.draw.circle(screen, ibody.color, loca(
            ibody.position, SCREEN_OFFSET), max(ibody.drawSize * ZOOM_SCALE * 2, 1))
        screen.blit(name, loca(ibody.position,SCREEN_OFFSET)+np.array([10, 0]))
        # screen.blit(spd, loca(ibody.position, SCREEN_OFFSET) + np.array([10, -10]))
        # screen.blit(pos, loca(ibody.position, SCREEN_OFFSET) + np.array([10, -20]))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
