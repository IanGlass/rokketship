import pygame

from models import Asteroid, Spaceship
from utils import load_sprite

class RokketShip:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()

        self.asteroids = [Asteroid((0, 0)) for _ in range(6)]
        self.spaceship = Spaceship((400, 300))

    def _get_game_objects(self):
        return [*self.asteroids, self.spaceship]

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

        is_key_pressed = pygame.key.get_pressed()

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
        self.spaceship.move(self.screen)

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

    # Updates display with any changes this tick
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        # Run the program at a set speed regardless of CPU speed
        self.clock.tick(60)
