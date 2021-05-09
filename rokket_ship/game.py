import pygame

from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite


class RokketShip:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()

        self.bullets = []
        self.asteroids = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

        [Asteroid(get_random_position(self.screen), self.asteroids.append) for _ in range(6)]

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Rokket Ship")

    # Handles user input on each tick
    def _handle_input(self):
        for event in pygame.event.get():
            # Press ESC to quit game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            # Handle ship rotation
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)

            # Handle ship acceleration
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    # Processes logic outside of user input
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Check each asteroid for spaceship collision
        if self.spaceship:
            self.spaceship.move(self.screen)
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    break

        # Process bullet-asteroid collision
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        # Remove bullets that are off screen
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

    # Updates display with any changes this tick
    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.spaceship:
            self.spaceship.draw(self.screen)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        # Run the program at a set speed regardless of CPU speed
        self.clock.tick(60)
