import pygame


# Models --------------------------------------------------------------


class Settings(object):
    """Basic settings"""

    def __init__(self):
        self.width = 1366
        self.height = 768
        self.fon = pygame.image.load("fon.jpg")
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.tick_rate = 10
        self.run = True
        self.classic_mode = True
        self.zombie_size = 20
        self.hero_size = 5
        self.zombie_color = (180, 0, 0)
        self.hero_color = (225, 225, 225)
        self.default_humans_number = 150
        self.default_zombies_number = 1
        self.turn_angle = 70
        self.correction_increase = 100
        self.pause = False


class Hero(object):
    """Hero settings"""

    def __init__(self, zombie_size=20, hero_size=10, zombie_color=(180, 0, 0),
                 hero_color=(225, 225, 225), x=683, y=384, zombie=False, angle=0, time_recover=1000, zombie_speed_dif=2):
        self.angle = angle
        self._zombie_speed_dif = zombie_speed_dif
        self.x = x
        self.y = y
        self.speed = 10
        self.time_recover = time_recover
        if zombie:
            self.speed *= zombie_speed_dif
        self._zombie_size = zombie_size
        self._hero_size = hero_size
        self.steps = []

        if zombie:
            self.size = self._zombie_size
        else:
            self.size = self._hero_size

        self._zombie_color = zombie_color
        self._hero_color = hero_color

        if zombie:
            self.color = self._zombie_color
        else:
            self.color = self._hero_color

        self.is_zombie = zombie
        self.hero_img_1 = pygame.image.load("beast_1.png")
        self.hero_img_2 = pygame.image.load("beast_2.png")
        self.hero_img_3 = pygame.image.load("beast_3.png")

    def become_zombie(self):
        """Settings if infected"""
        if not self.is_zombie:
            self.is_zombie = True
            self.size = self._zombie_size
            self.color = self._zombie_color
            self.speed *= self._zombie_speed_dif

    def become_human(self):
        """Settings if recovered"""
        if self.is_zombie:
            self.is_zombie = False
            self.size = self._hero_size
            self.color = self._hero_color
            self.speed /= self._zombie_speed_dif


    def add_step(self, step: tuple):
        """ step example (50, 80)"""
        self.steps.append(step)
        if len(self.steps) > 10:
            self.steps = self.steps[1:]


class Population:
    """Population control"""
    def __init__(self):
        self.people_list = []

    def add_hero(self, hero: Hero):
        self.people_list.append(hero)

    def remove_hero(self, hero: Hero):
        if hero in self.people_list:
            self.people_list.remove(hero)
        else:
            print('ALARM! Hero not in list to delete')

    def check_ballance(self) -> tuple:
        zombies = 0
        heroes = 0
        for hero in self.people_list:
            if hero.is_zombie:
                zombies += 1
            else:
                heroes += 1

        return heroes, zombies
