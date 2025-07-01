from random import choice, randint
import pygame


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
        grid_size = 20
        grid_width = 640 // grid_size
        grid_height = 480 // grid_size
        self.position = (
            randint(0, grid_width - 1) * grid_size,
            randint(0, grid_height - 1) * grid_size
        )

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности.
            Args:
            screen: Поверхность для отрисовки.
        """
        rect = pygame.Rect(self.position, (20, 20))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()
        self.body_color = (0, 255, 0)  # Зеленый цвет
        self.positions = [(320, 240)]  # Центр экрана
        self.direction = (1, 0)  # Начальное направление - вправо
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
        new_x = (head_x + dir_x * 20) % 640
        new_y = (head_y + dir_y * 20) % 480
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
        self.positions = [(320, 240)]
        self.length = 1
        self.direction = choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def draw(self, screen):
        """Отрисовывает змейку на экране.
        Args:
            screen: Поверхность для отрисовки.
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (20, 20))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, (93, 216, 228), rect, 1)

        head_rect = pygame.Rect(self.positions[0], (20, 20))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, (93, 216, 228), head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (20, 20))
            pygame.draw.rect(screen, (0, 0, 0), last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой.
    Args:
        game_object: Объект змейки, которым управляем.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif (event.key == pygame.K_UP 
                  and game_object.direction != (0, 1)):
                game_object.next_direction = (0, -1) 
            elif (event.key == pygame.K_DOWN 
                  and game_object.direction != (0, -1)):
                game_object.next_direction = (0, 1)
            elif (event.key == pygame.K_LEFT 
                  and game_object.direction != (1, 0)):
                game_object.next_direction = (-1, 0)
            elif (event.key == pygame.K_RIGHT 
                  and game_object.direction != (-1, 0)):
                game_object.next_direction = (1, 0)
            elif event.key == pygame.K_SPACE:
                # Пауза при нажатии пробела
                paused = True
                while paused:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                        if (e.type == pygame.KEYDOWN 
                                and e.key == pygame.K_SPACE):
                            paused = False


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

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

        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
