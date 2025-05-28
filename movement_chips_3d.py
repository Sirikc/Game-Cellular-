import numpy as np
import sqlite3
import json
import copy
# Создаем массив с dtype=object
playing_arena = np.array(
    [
        [np.array([0]), np.array([3, 0, 1]), np.array([0])],
        [np.array([0]), np.array([0]), np.array([0])],
        [np.array([0]), np.array([0]), np.array([0])],
        [np.array([0]), np.array([0]), np.array([0])]
    ],
    dtype=object
)


def find_element_coordinates(matrix, search_value):
    """
    Находит координаты первого вхождения элемента search_value в двумерном массиве matrix.

    Параметры:
    matrix (np.ndarray): Двумерный массив.
    search_value: Значение, которое нужно найти.

    Возвращает:
    list or None: Список с координатами [строка, столбец, индекс в подмассиве] или None, если элемент не найден.
    """
    for row in range(matrix.shape[0]):  # Перебор строк
        for col in range(matrix.shape[1]):  # Перебор столбцов
            if search_value in matrix[row, col]:  # Проверяем, есть ли значение в подмассиве
                subarray = np.where(matrix[row, col] == search_value)[0][0]  # Индекс в подмассиве
                return [row, col, subarray]  # Возвращаем координаты


def move_element_numpy(matrix, old_coordinates, new_coordinates):
    """
    Перемещает элемент из позиции (old_coordinates) в позицию (new_coordinates)
    в NumPy массиве.
    Принимает массив из [позиция в подмассиве, строка, ряд]
    """
    matrix = copy.deepcopy(matrix)
    new_row = new_coordinates[0]
    new_col = new_coordinates[1]
    old_row, old_col, old_subarray = old_coordinates

    if new_row < 0:
        new_row = 0
        old_row = 1
    if new_col < 0:
        new_col = 0
        old_col = 1
    
    element = matrix[old_row, old_col][old_subarray]
    matrix[old_row, old_col] = np.delete(matrix[old_row, old_col], old_subarray)
    matrix[new_row, new_col] = np.append(matrix[new_row, new_col], element)
    return matrix


def matrix_expansion(matrix, fill_value, direction_of_expansion):
    """
    Расширяет матрицу, работая с данными через списки Python для полного контроля размерности.
    """
    # Преобразуем матрицу в список списков
    matrix_list = matrix.tolist()
    rows = len(matrix_list)
    cols = len(matrix_list[0]) if rows > 0 else 0

    if direction_of_expansion == "Right":
        for row in matrix_list:
            row.append(fill_value.copy())
    
    elif direction_of_expansion == "Left":
        for row in matrix_list:
            row.insert(0, fill_value.copy())
    
    elif direction_of_expansion == "Down":
        new_row = [fill_value.copy() for _ in range(cols)]
        matrix_list.append(new_row)
    
    elif direction_of_expansion == "Up":
        new_row = [fill_value.copy() for _ in range(cols)]

        matrix_list.insert(0, new_row)
    
    # Возвращаем новую матрицу с сохранением типа элементов
    return np.array(matrix_list, dtype=object)

def move_chip(matrix, command, old_coordinates):
        global new_coordinates
        if command == "Up":
            new_coordinates = [old_coordinates[0]-1, old_coordinates[1], old_coordinates[2]]
            if new_coordinates[0] >= 0:
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
            else:
                matrix = matrix_expansion(matrix, np.array([2]), "Up")
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
        elif command == "Down":
            new_coordinates = [old_coordinates[0]+1, old_coordinates[1], old_coordinates[2]]
            if old_coordinates[0] < matrix.shape[0]-1:
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
            else:
                matrix = matrix_expansion(matrix, np.array([2]), "Down")
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
        elif command == "Left":
            new_coordinates = [old_coordinates[0], old_coordinates[1]-1, old_coordinates[2]]
            if new_coordinates[1] >= 0:
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
            else:
                matrix = matrix_expansion(matrix, np.array([2]), "Left")
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
        elif command == "Right":
            new_coordinates = [old_coordinates[0], old_coordinates[1]+1, old_coordinates[2]]
            if new_coordinates[1] < matrix.shape[1]:
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
            else:
                matrix = matrix_expansion(matrix, np.array([2]), "Right")
                matrix = move_element_numpy(matrix, old_coordinates, new_coordinates)
        return matrix

def main(matrix, chip_uid, chip_move):
    """
    matrix - поле, в котором мы перемещаем фишку
    chip_uid - номер фишки, которую надо передвинуть
    chip move - последовательность передвижений фишки. В качестве аргумента может принимать массив из направлений движения (Up, Down, Left, Right).
        Или номер строки из БД database_movements. для добавления строки использовать команду:
        cursor.execute("INSERT INTO movement (move) VALUES (?)", (json.dumps(["Up", "Up"]),))
        для вывода:
        cursor.execute("SELECT * FROM movement WHERE ROWID=?", (row_number,))
        row = cursor.fetchone()
        restored_array = json.loads(row[0])
    """
    global new_coordinates
    crossings_count = 0 #кол-во прохожденных клеток с 2
    old_matrix = matrix #выводим если пользователь отказался ходить
    
    if type(chip_move) == int: #если в качестве передвижения мы передаем целое число (номер строки в database_movements)
        connection = sqlite3.connect('Scripts/database_movements.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movement WHERE ROWID=?", (chip_move,))
        row = cursor.fetchone()
        restored_array = json.loads(row[0])
        connection.close()
        return main(matrix, chip_uid, restored_array)
    else:
        for i in chip_move:
        
            old_coordinates = find_element_coordinates(matrix, chip_uid)
            matrix = move_chip(matrix, i, old_coordinates)
            if new_coordinates[0] < 0:
                new_coordinates[0] = 0
            if new_coordinates[1] < 0:
                new_coordinates[1] = 0
            if np.any(matrix[new_coordinates[0]][new_coordinates[1]] == 2):
                crossings_count += 1
    
        return {"matrix": np.array(matrix), "crossings": crossings_count}

# print(main(playing_arena, 1, 2))
# print(playing_arena)