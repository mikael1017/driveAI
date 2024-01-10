import pygame
import os
import math
import sys
import neat

SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TRACK = pygame.image.load(os.path.join("Assets", "track.png"))
VELOCITY_MULTIPLIER = 6
GRASS_COLOR = (2, 105, 31, 255)
ANGLE_FROM_CENTER_TO_HEADLIGHT = 18
RADAR_LENGTH = 200


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(
            os.path.join("Assets", "car.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(490, 820))
        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotational_vel = 5
        self.direction = 0
        self.alive = True

    def update(self):
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()

    def drive(self):
        if self.drive_state:
            self.rect.center += self.vel_vector * VELOCITY_MULTIPLIER

    def collision(self):
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + ANGLE_FROM_CENTER_TO_HEADLIGHT))
                                     * length), int(self.rect.center[1] - math.sin(math.radians(self.angle + ANGLE_FROM_CENTER_TO_HEADLIGHT)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - ANGLE_FROM_CENTER_TO_HEADLIGHT))
                                    * length), int(self.rect.center[1] - math.sin(math.radians(self.angle - ANGLE_FROM_CENTER_TO_HEADLIGHT)) * length)]

        if SCREEN.get_at((collision_point_right)) == pygame.Color(GRASS_COLOR) or SCREEN.get_at((collision_point_left)) == pygame.Color(GRASS_COLOR):
            self.alive = False

        pygame.draw.circle(SCREEN, (0, 255, 0, 0), collision_point_right, 3)
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), collision_point_left, 3)

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotational_vel
            self.vel_vector.rotate_ip(self.rotational_vel)
        if self.direction == -1:
            self.angle += self.rotational_vel
            self.vel_vector.rotate_ip(-self.rotational_vel)
        self.image = pygame.transform.rotozoom(
            self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while not SCREEN.get_at((x, y)) == pygame.Color(GRASS_COLOR) and length < RADAR_LENGTH:
            length += 1
            x = int(self.rect.center[0] +
                    math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] -
                    math.sin(math.radians(self.angle + radar_angle)) * length)

        pygame.draw.line
        # draw radar
        pygame.draw.line(SCREEN, (255, 255, 255, 255),
                         self.rect.center, (x, y))
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 3)

        # we can find the distance from the car center to the point of collision
        # using the distance formula
        # distance = math.sqrt((self.rect.center[0] - x)
        #                      ** 2 + (self.rect.center[1] - y)**2)


car = pygame.sprite.GroupSingle(Car())


def eval_genomes():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))
        car.draw(SCREEN)

        # User Input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            car.sprite.direction = 0

        # Drive
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = True

        # Rotate
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1

        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1

        # Update
        car.draw(SCREEN)
        car.update()
        pygame.display.update()


eval_genomes()
