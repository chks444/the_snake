import pygame
import random


# КОНСТАНТЫ
# Размеры поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480       # Размер окна
CENTRAL_POS = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))  # Центральная точка
GRID_SIZE = 20                               # Размер одной клетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE       # Ширина окна в клетках (32)
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE     # Высота окна в клетках (24)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Фон - черный
BORDER_COLOR = (93, 216, 228)       # Грани ячейки - серый
APPLE_COLOR = (255, 0, 0)           # Яблоко - красный
SNAKE_COLOR = (0, 255, 0)           # Змейка - зеленый
# Скорость змейки
SPEED = 20

# НАСТРОЙКИ PYTEST
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка 444')
clock = pygame.time.Clock()


class GameObject():
    """
    Базовый класс для игровых объектов.

    Содержит общие атрибуты, такие как позиция и цвет, которые
    описывают игровые объекты. Также включает в себя заготовку метода draw
    для отрисовки объекта на игровом поле.

    Предназначен для наследования другими игровыми объектами, чтобы
    они могли использовать функциональность и расширять её.
    """

    def __init__(self):
        self.position = CENTRAL_POS
        self.body_color = None

    def draw(self):
        """
        Абстрактный метод, который предназначен для
        переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Описывает яблоко и действия c ним.

    Отображает яблоко в случайных клетках игрового поля.
    """

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Описывает змейку и её поведение.

    Управляет её движением, отрисовкой,
    также обрабатывает действия пользователя.
    """

    def __init__(self):
        self.length = 1
        self.positions = [CENTRAL_POS]
        self.position = self.positions[0]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head_pos = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                        (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_pos)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTRAL_POS]
        directions = [UP, DOWN, LEFT, RIGHT]
        rand_irections = random.choice(directions)
        self.direction = rand_irections


def main():
    """Основной игровой цикл"""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(5)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
