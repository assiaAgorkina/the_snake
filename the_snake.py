from random import choice, randint
import pygame

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize pygame and create screen and clock
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position if position else (0, 0)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = (255, 0, 0)  # Красный цвет
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()
        self.body_color = (0, 255, 0)  # Зеленый цвет
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, (93, 216, 228), rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, (93, 216, 228), head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_quit_event(event):
    """Обрабатывает событие выхода из игры."""
    if (event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE)):
        pygame.quit()
        raise SystemExit
    return False


def handle_direction_change(event, game_object):
    """Обрабатывает изменение направления движения змейки."""
    direction_map = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT
    }
    opposite_directions = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }
    if event.key in direction_map:
        new_direction = direction_map[event.key]
        if game_object.direction != opposite_directions.get(new_direction):
            game_object.next_direction = new_direction
            return True
    return False


def handle_pause():
    """Обрабатывает паузу в игре."""
    paused = True
    while paused:
        for e in pygame.event.get():
            if handle_quit_event(e):
                return
            if (e.type == pygame.KEYDOWN
                    and e.key == pygame.K_SPACE):
                paused = False


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if handle_quit_event(event):
            continue
        if event.type == pygame.KEYDOWN:
            if handle_direction_change(event, game_object):
                continue
            if event.key == pygame.K_SPACE:
                handle_pause()


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.display.set_caption('Змейка')
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(20)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
