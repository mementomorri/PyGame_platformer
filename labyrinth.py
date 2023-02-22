from pygame import *


# Объявление параметров программы в виде констант
GAME_DELAY = 50
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 960

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VELOCITY = 10

VICTORY_HEIGHT = 90
VICTORY_WIDTH = 90

OBSTACLE_WIDTH = 75
OBSTACLE_HEIGHT = 75
OBSTACLE_VELOCITY = 7

BULLET_WIDTH = 55
BULLET_HEIGHT = 55
BULLET_VELOCITY = 15


class GameSprite(sprite.Sprite):
    """
    Корневой класс прародитель. В исходном виде пригоден для отрисовки статичных и не подвижных объектов,
    в формате изображений.
    Весьма полезен к наследованию игровыми спрайтами, поскольку обладает шаблонным наборов свойств и методом
    для отрсовки.
    """
    def __init__(self, picture_path: str, sprite_width: int, sprite_height: int, x_coord: int, y_coord: int):
        """
        Конструктор класса GameSprite.
        :param picture_path: путь к изображению выводящемуся на спрайте
        :param sprite_width: ширина спрайта (в пикселях)
        :param sprite_height: высота спрайта (в пикселях)
        :param x_coord: положение спрайта по горизонтали (от левого верхнего угла окна)
        :param y_coord: положение спрайта по вертикали (от левого верхнего угла окна)
        """
        super().__init__()
        self.image = transform.scale(image.load(picture_path), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = y_coord

    def reset(self, window: Surface) -> None:
        """
        Удобный метод для отрисовки спрайта в указанном окне.
        :param window: окошко, в котором нужно отрисовать спрайт
        """
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    """
    Класс репрезентация управляемого игроком персонажа. Наследник класса GameSprite, обладает всеми его свойствами и
    методами. Помимо наследуюемых свойств имеет скорость перемещения по горизонтали и вертикали. А также, имеет методы
    для обновления текущего положения спрайта в зависимости от направления движения и выстрелы снарядов.
    """
    def __init__(self, picture_path: str, sprite_width: int, sprite_height: int, x_coord: int, y_coord: int,
                 x_velocity: int = 0, y_velocity: int = 0):
        """
        Конструктор класса Player.
        :param picture_path: путь к изображению выводящемуся на спрайте
        :param sprite_width: ширина спрайта (в пикселях)
        :param sprite_height: высота спрайта (в пикселях)
        :param x_coord: положение спрайта по горизонтали (от левого верхнего угла окна)
        :param y_coord: положение спрайта по вертикали (от левого верхнего угла окна)
        :param x_velocity: скорость передвижения по горизонтали (в пикселях)
        :param y_velocity: скорость передвижения по вертикали (в пикселях)
        """
        GameSprite.__init__(self, picture_path, sprite_width, sprite_height, x_coord, y_coord)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def update(self, barriers: sprite.Group) -> None:
        """
        Метод обновления позиции управляемого спрайта в окне игры. Ограничивает выход за пределы экрана игры
        и не дает проходить сквозь стены с помощью обработки столкновений.
        :param barriers: гуппа спрайтов стен или не проходимых для игрока барьеров.
        """
        if self.rect.x <= WINDOW_WIDTH - PLAYER_WIDTH and self.x_velocity > 0 or self.rect.x >= 0 > self.x_velocity:
            self.rect.x += self.x_velocity
        if self.rect.y <= WINDOW_HEIGHT - PLAYER_HEIGHT and self.y_velocity > 0 or self.rect.y >= 0 > self.y_velocity:
            self.rect.y += self.y_velocity

        platforms_touched = sprite.spritecollide(self, barriers, False)
        if len(platforms_touched) > 0:
            if self.x_velocity > 0:
                self.rect.x -= PLAYER_VELOCITY
                self.x_velocity = 0
            elif self.x_velocity < 0:
                self.rect.x += PLAYER_VELOCITY
                self.x_velocity = 0
            if self.y_velocity > 0:
                self.rect.y -= PLAYER_VELOCITY
                self.y_velocity = 0
            elif self.y_velocity < 0:
                self.rect.y += PLAYER_VELOCITY
                self.y_velocity = 0

    def fire(self, bullets: sprite.Group) -> None:
        """
        Метод для выстрела снарядов из спрайта игрока. Снаряды добавляются в группу спрайтов и отрисовываются в
        игровом цикле.
        :param bullets: группа спрайтов, в которую добавляется  снаряд для дальнейшей отрисовки
        """
        bullets.add(Bullet('img/bullet.png', BULLET_WIDTH, BULLET_HEIGHT, self.rect.left - 10, self.rect.centery - 30,
                           BULLET_VELOCITY))


class Obstacle(GameSprite):
    """
    Спрайт препятствие, преграждающее путь к победному спрайту. Если игрок на него наступит, то игра будет считаться
    завершенной и отобразится экран поражения. Помимо наследуемых от класса GameSprite свойств, также имеет свойства
    скорости передвижения и направление движения. А также, имеет метод обновления положения на экране. По поведению
    похож на класс Player, за исключением того, что он не управляется игроком, а двигается автономно.
    """
    def __init__(self, picture_path: str, sprite_width: int, sprite_height: int, x_coord: int, y_coord: int,
                 velocity: int):
        """
        Конструктор класса Obstacle.
        :param picture_path: путь к изображению выводящемуся на спрайте
        :param sprite_width: ширина спрайта (в пикселях)
        :param sprite_height: высота спрайта (в пикселях)
        :param x_coord: положение спрайта по горизонтали (от левого верхнего угла окна)
        :param y_coord: положение спрайта по вертикали (от левого верхнего угла окна)
        :param velocity: скорость передвижения препятствия (в пикселях)
        """
        GameSprite.__init__(self, picture_path, sprite_width, sprite_height, x_coord, y_coord)
        self.velocity = velocity
        self.direction = str  # Направление движения

    def update(self) -> None:
        """
        Метод обновления положения препятствия и изменения направления в случае достижения крайней точки маршрута.
        Препятствие перемещается по вертикали. Предназначен для применения в игровом цикле.
        """
        if self.rect.y <= 340:
            self.direction = 'bottom'
        if self.rect.y >= WINDOW_HEIGHT - 80:
            self.direction = 'top'
        if self.direction == 'top':
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity


class Bullet(GameSprite):
    """
    Спрайт снаряд, используемый для взаимодействия игрока с окружающим миром, в частности для избаления от препятствий.
    Помимо наследуемых от класса GameSprite свойств, также имеет свойство
    скорости передвижения. А также, имеет метод обновления положения на экране. При выходе за пределы экрана исчезает
    из игры с помощью метода kill.
    """
    def __init__(self, picture_path: str, sprite_width: int, sprite_height: int, x_coord: int, y_coord: int,
                 velocity: int):
        """
        Конструктор класса Bullet.
        :param picture_path: путь к изображению выводящемуся на спрайте
        :param sprite_width: ширина спрайта (в пикселях)
        :param sprite_height: высота спрайта (в пикселях)
        :param x_coord: положение спрайта по горизонтали (от левого верхнего угла окна)
        :param y_coord: положение спрайта по вертикали (от левого верхнего угла окна)
        :param velocity: скорость передвижения снаряда (в пикселях)
        """
        GameSprite.__init__(self, picture_path, sprite_width, sprite_height, x_coord, y_coord)
        self.velocity = velocity

    def update(self) -> None:
        """
        Метод обновления положения снаряда. При выходе за пределы экрана удаляется с помощью метода kill.
        """
        self.rect.x -= self.velocity
        if self.rect.x < -BULLET_WIDTH/2:
            self.kill()


def run_game() -> None:
    """
    Запуск игрового цикла.
    :rtype: None
    """

    # Введение ключевых переменных
    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.set_caption('Лабиринт')
    game_over = False
    run = True

    player = Player('img/player.png', PLAYER_WIDTH, PLAYER_WIDTH, 5, 100, 0, 0)
    background = GameSprite('img/background.jpg', WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)
    victory = GameSprite('img/finish.png', VICTORY_WIDTH, VICTORY_HEIGHT, 30, 500)
    victory_pic = GameSprite('img/victory_pic.png', WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)
    fail_pic = GameSprite('img/fail_pic.png', WINDOW_WIDTH, WINDOW_HEIGHT, 0, 0)

    bullets = sprite.Group()
    barriers = sprite.Group()
    obstacles = sprite.Group()
    obstacles.add(
        Obstacle('img/obstacle.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT, 325, 560, OBSTACLE_VELOCITY)
    )
    barriers.add(
        GameSprite('img/wall_1.jpg', 60, 125, 200, 0),
        GameSprite('img/wall_1.jpg', 400, 60, 200, 125),
        GameSprite('img/wall_1.jpg', 300, 60, 0, 300),
        GameSprite('img/wall_1.jpg', 60, 125, 240, 360),
        GameSprite('img/wall_1.jpg', 60, 180, 240, 610),
        GameSprite('img/wall_3.jpg', 60, 200, 680, 200),
        GameSprite('img/wall_3.jpg', 60, 200, 680, 450),
        GameSprite('img/wall_3.jpg', 150, 60, 740, 450)
    )

    # Игровой цикл
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            # Обработка нажатий кнопок клавиатуры
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False
                if e.key == K_r:
                    run = False
                    run_game()
                if e.key == K_UP or e.key == K_w:
                    player.y_velocity -= PLAYER_VELOCITY
                if e.key == K_DOWN or e.key == K_s:
                    player.y_velocity += PLAYER_VELOCITY
                if e.key == K_LEFT or e.key == K_a:
                    player.x_velocity -= PLAYER_VELOCITY
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_velocity += PLAYER_VELOCITY
                if e.key == K_SPACE:
                    player.fire(bullets)
            elif e.type == KEYUP:
                if e.key == K_UP or e.key == K_w:
                    player.y_velocity = 0
                if e.key == K_DOWN or e.key == K_s:
                    player.y_velocity = 0
                if e.key == K_LEFT or e.key == K_a:
                    player.x_velocity = 0
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_velocity = 0
        if not game_over:
            # Отрисовка спрайтов игры
            background.reset(window)
            victory.reset(window)
            player.update(barriers)
            player.reset(window)

            barriers.draw(window)
            obstacles.update()
            obstacles.draw(window)
            bullets.update()
            bullets.draw(window)
            # Обработка столкновения снарядов со стенами и препятствиями (монстриками)
            sprite.groupcollide(bullets, barriers, True, False)
            sprite.groupcollide(bullets, obstacles, True, True)
            # Проверка условий завершения игры
            if sprite.collide_rect(player, victory) or sprite.spritecollide(player, obstacles, False):
                game_over = True
        if game_over:
            # Отрисовка экрана победы или поражения
            if sprite.collide_rect(player, victory):
                victory_pic.reset(window)
            else:
                fail_pic.reset(window)
        time.delay(GAME_DELAY)
        display.update()


if __name__ == '__main__':
    run_game()
