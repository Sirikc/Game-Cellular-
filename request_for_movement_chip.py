import requests
import pygame
import sys
def request_for_movement_chip(chip_uid, chip_move):
    return requests.post("http://127.0.0.1:5000/api/movement_chip", json={"chip_uid": chip_uid, "chip_move": chip_move}).json()
# print(request_for_movement_chip(1, 1))

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Visualization")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)

# Размеры клетки
CELL_SIZE = 80
CELL_MARGIN = 5

# Шрифт
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

def draw_matrix(matrix, crossings):
    """Отрисовывает матрицу с вложенными массивами.
    
    Args:
        matrix: 2D-матрица, где каждая клетка — это список чисел.
        crossings: число пересечений (для отображения внизу).
    """
    screen.fill(WHITE)
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            x = col * (CELL_SIZE + CELL_MARGIN) + 50
            y = row * (CELL_SIZE + CELL_MARGIN) + 50
            
            # Рисуем клетку
            pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2)
            
            # Получаем массив из клетки
            cell_data = matrix[row][col]
            
            # Отображаем элементы в столбик
            for i, value in enumerate(cell_data):
                text = small_font.render(str(value), True, BLACK)
                text_rect = text.get_rect(
                    center=(x + CELL_SIZE // 2, y + 20 + i * 25)
                )
                screen.blit(text, text_rect)
    
    # Выводим количество пересечений
    crossings_text = font.render(f"Crossings: {crossings}", True, BLACK)
    screen.blit(crossings_text, (50, HEIGHT - 50))

# Ваши данные
data = request_for_movement_chip(1, 2)

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Передаём матрицу и crossings в функцию отрисовки
    draw_matrix(data['Result']['matrix'], data['Result']['crossings'])
    pygame.display.flip()

pygame.quit()
sys.exit()