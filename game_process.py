import pygame
from statistics import *
from models import *
import random
import math

# Game process --------------------------------------------------------------


def get_distance_from_objects(x1, x2, y1, y2) -> float:
    """input coordinates of 2 objects to get distance between"""
    x = x1 - x2
    y = y1 - y2
    distance = (x ** 2 + y ** 2) ** 0.5
    return distance


class Game_process(object):
    """General process"""
    def __init__(self):
        self.settings = Settings()
        self.population = Population()
        self.graph = Graph()
        self.game_status = True
        self.turn_count_for_writen = 0
        self.count = 0
        self.count_2 = 0

        # make population here
        for i in range(self.settings.default_humans_number):
            self.population.add_hero(Hero(
                zombie_size=self.settings.zombie_size,
                hero_size=self.settings.hero_size,
                zombie_color=self.settings.zombie_color,
                hero_color=self.settings.hero_color,
                x=random.randint(1, self.settings.width - 1),
                y=random.randint(1, self.settings.height - 1),
                zombie=False,
                angle=random.randint(0, 359),
                time_recover=10
            )
            )

        for i in range(self.settings.default_zombies_number):
            self.population.add_hero(Hero(
                zombie_size=self.settings.zombie_size,
                hero_size=self.settings.hero_size,
                zombie_color=self.settings.zombie_color,
                hero_color=self.settings.hero_color,
                x=random.randint(0, self.settings.width - 1),
                y=random.randint(0, self.settings.height - 1),
                zombie=True,
                angle=random.randint(0, 359))
            )

    def draw_hero(self, hero: Hero):
        if hero.steps:
            start = (hero.x, hero.y)
            for step in hero.steps[::-1]:
                finish = step
                pygame.draw.line(self.settings.screen, hero.color, start, finish, 2)
                start = step
        pygame.draw.circle(self.settings.screen, hero.color, (int(hero.x), int(hero.y)), hero.size)

        angle = hero.angle

        dx = math.cos(math.radians(angle))
        dy = math.sin(math.radians(angle))
        if 0 <= hero.x + dx * hero.speed < self.settings.width and 0 <= hero.y + dy * hero.speed <= self.settings.height:
            line_x = hero.x + dx * hero.speed
            line_y = hero.y + dy * hero.speed
            start = (hero.x, hero.y)
            finish = (line_x, line_y)
            dx_1 = math.cos(math.radians(angle - self.settings.turn_angle))
            dy_1 = math.sin(math.radians(angle - self.settings.turn_angle))
            line_x_1 = hero.x + dx_1 * hero.speed
            line_y_1 = hero.y + dy_1 * hero.speed
            pygame.draw.line(self.settings.screen, (255, 255, 0), start, finish, 2)
            pygame.draw.line(self.settings.screen, (255, 255, 255), start, (line_x_1, line_y_1), 2)
            dx_2 = math.cos(math.radians(angle + self.settings.turn_angle))
            dy_2 = math.sin(math.radians(angle + self.settings.turn_angle))
            line_x_2 = hero.x + dx_2 * hero.speed
            line_y_2 = hero.y + dy_2 * hero.speed
            pygame.draw.line(self.settings.screen, (225, 255, 225), start, (line_x_2, line_y_2), 2)

    def collision(self, hero: Hero):
        for target in self.population.people_list:
            if hero != target:
                distance = get_distance_from_objects(hero.x,
                                                    target.x,
                                                    hero.y,
                                                    target.y)
                if distance <= hero.size + target.size:
                    if hero.is_zombie and not target.is_zombie:
                        target.become_zombie()

    def game_cycle(self):
        """Cycle game"""
        if self.game_status:
            self.settings.screen.blit(self.settings.fon, (0, 0))

            self.settings.clock.tick(self.settings.tick_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
            elif keys[pygame.K_SPACE]:
                self.settings.pause = not self.settings.pause

            # hero move
            for indexhero, hero in enumerate(self.population.people_list):
                # hero draw
                self.draw_hero(hero)
                if not self.settings.pause:
                    if self.settings.classic_mode and self.settings.run:  # movement of objects
                        correction = 0
                        delta_angle = random.randint(-self.settings.turn_angle,
                                                     self.settings.turn_angle)
                        angle = (hero.angle + delta_angle) % 360
                        while True:
                            dx = math.cos(math.radians(angle + correction))
                            dy = math.sin(math.radians(angle + correction))
                            if 0 <= hero.x + dx * hero.speed < self.settings.width and 0 <= hero.y + dy * hero.speed <= \
                                    self.settings.height:
                                hero.add_step((hero.x, hero.y))
                                hero.x += dx * hero.speed
                                hero.y += dy * hero.speed
                                hero.angle = angle
                                if hero.is_zombie:
                                    hero.time_recover -= 1
                                    if hero.time_recover == 0:
                                        hero.become_human()
                                        hero.time_recover = 10

                                self.collision(hero)
                                break
                            else:
                                correction += self.settings.correction_increase
            if self.turn_count_for_writen == 0:
                with open('records.csv', "w") as file:
                    file.write("turn,heroes,zombies\n")
            with open('records.csv', "a") as file:
                balance = self.population.check_ballance()
                file.write(f"{self.turn_count_for_writen},{balance[0]},{balance[1]}\n")
                if balance[0] == 0:
                    self.game_status = False
            self.turn_count_for_writen += 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
            if self.count == 0:
                self.graph.create_graph()
                self.count = 1
            self.photo = pygame.image.load("Figure_1.png")
            self.fon = pygame.transform.scale(self.photo, (self.settings.width, self.settings.height))
            self.settings.screen.blit(self.fon, (0, 0))
        pygame.display.update()

    def start(self):
        while self.settings.run:
            self.game_cycle()
        pygame.init()
