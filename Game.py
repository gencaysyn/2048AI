import numpy as np
import random
import msvcrt  # enter tuşunu kullanmadan input almak için bir kütüphane
import math


# Tablo oluşturma fonksiyonu önce matrisi oluşturuyor
# daha sonra 2 noktaya rasgele 2 atıyor
def create_table(n):
    mat = np.zeros((n, n), dtype=int)
    count = 0
    while count != 2:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if mat[i][j] == 0:
            mat[i][j] = 2
            count += 1
    return mat


# Yeni gelecek sayıları atayan fonksiyon eğer tabloda boş yer varsa
# bu yere 2 veya 4 atıyor
def generate_number(mat):
    if empty_box(mat) == 0:
        return

    i = random.randint(0, len(mat) - 1)
    j = random.randint(0, len(mat) - 1)

    if mat[i][j] == 0:
        number = random.randint(0, 1)
        if number == 0:
            mat[i][j] = 2
        else:
            mat[i][j] = 4
        return
    return generate_number(mat)


# matriste değişim olup olmadığını kontrol eden fonksiyon
def are_same(A, B):
    for i in range(4):
        for j in range(4):
            if A[i][j] != B[i][j]:
                return False
    return True


# Hareket etme fonksiyonu oldukça karmaşık bir yapıda.
# Dönülmesi gereken yöne göre önce ardışık denk gelen ve aynı olan sayılar toplanıyor,
# sonra verilen yöne doğru tüm sayılar kaydırılıyor.
# İşlem sonunda bir değişiklik olmazsa fonksiyon false dödürüyor.
def move(mat, way):
    change = mat.copy()
    if way == "left":
        for i in range(len(mat)):
            index = 0
            cursor = mat[i][index]
            j = 1
            while j < len(mat[i]):
                if mat[i][j] != 0:
                    if cursor == mat[i][j]:
                        mat[i][index] = cursor * 2
                        mat[i][j] = 0
                        index = j
                        cursor = mat[i][index]
                    else:
                        index = j
                        cursor = mat[i][index]
                j += 1

            # Slider
            write = False
            t = 0
            buffer = [0] * len(mat)
            for k in range(len(mat[i])):
                if mat[i][k] != 0:
                    write = True
                    buffer[t] = mat[i][k]
                    t += 1
            if write:
                mat[i][:] = buffer

    elif way == "up":
        for i in range(len(mat)):
            index = 0
            cursor = mat[index][i]
            j = 1
            while j < len(mat[i]):
                if mat[j][i] != 0:
                    if cursor == mat[j][i]:
                        mat[index][i] = cursor * 2
                        mat[j][i] = 0
                        index = j
                        cursor = mat[index][i]
                    else:
                        index = j
                        cursor = mat[index][i]
                j += 1

            # Slider
            write = False
            t = 0
            buffer = [0] * len(mat)
            for k in range(len(mat[i])):
                if mat[k][i] != 0:
                    write = True
                    buffer[t] = mat[k][i]
                    t += 1
            if write:
                for t in range(len(buffer)):
                    mat[t][i] = buffer[t]
    elif way == "down":
        for i in range(len(mat)):
            index = len(mat) - 1
            cursor = mat[index][i]
            j = len(mat) - 2
            while j >= 0:
                if mat[j][i] != 0:
                    if cursor == mat[j][i]:
                        mat[index][i] = cursor * 2
                        mat[j][i] = 0
                        index = j
                        cursor = mat[index][i]
                    else:
                        index = j
                        cursor = mat[index][i]
                j -= 1

            # Slider
            write = False
            t = 0
            buffer = [0] * len(mat)
            for k in range(len(mat[i]) - 1, -1, -1):
                if mat[k][i] != 0:
                    write = True
                    buffer[t] = mat[k][i]
                    t += 1
            if write:
                for t in range(len(mat[i]) - 1, -1, -1):
                    mat[t][i] = buffer[len(mat[i]) - t - 1]

    elif way == "right":
        for i in range(len(mat)):
            index = len(mat) - 1
            cursor = mat[i][index]
            j = len(mat) - 2
            while j >= 0:
                if mat[i][j] != 0:
                    if cursor == mat[i][j]:
                        mat[i][index] = cursor * 2
                        mat[i][j] = 0
                        index = j
                        cursor = mat[i][index]
                    else:
                        index = j
                        cursor = mat[i][index]
                j -= 1
            # Slider
            write = False
            t = len(mat) - 1
            buffer = [0] * len(mat)
            for k in range(len(mat[i]) - 1, -1, -1):
                if mat[i][k] != 0:
                    write = True
                    buffer[t] = mat[i][k]
                    t -= 1
            if write == True:
                mat[i][:] = buffer
    else:
        print("Way Error!")
    return not are_same(mat, change)


def is_end(mat):
    change = mat.copy()
    if move(change, "left") or move(change, "up") or move(change, "right") or move(change, "down"):
        return False
    print("Game Over")
    return True


############################################################
############# Fitness Functions ############################
############################################################

# Boş kutuları sayan fonksiyon
def empty_box(mat):
    result = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 0:
                result += 1
    return result


# kayda değer bir fark yaratması için  sayıların küplerinin toplamını alan fonksiyon
def sum_box(mat):
    result = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] != 0:
                result += mat[i][j] ** 3
    return result


# Eski uzaklık hesaplaytan fonksiyon
# Sayıların merkeze olan uzaklığını sayıyla çarpıp döndürür
# def dist_center(mat):
#     result = 0
#     for i in range(len(mat)):
#         for j in range(len(mat[i])):
#             result += (mat[i][j]) * (abs(i - 1.5) + abs(j - 1.5))
#     return -result


# Sayıların sol alt köşeye uzaklalıların sayıyla çarpımını döndürür
def dist_center(mat):
    result = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] != 0:
                result += (mat[i][j]) * (abs(i - 3) + abs(j - 0))
    return -result

def dist_edge(mat):
    result = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] != 0:
                result += (mat[i][j]) * (abs(i - 3))
    return -result

# Aynı olan sayıların birbirlerine olan uzaklıklarının sayılardan birinin çarpımını döndürür
def dist_equals(matrix):
    my_map = {}
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                try:
                    p = my_map[matrix[i][j]]
                    result += (abs(i - p[0]) + abs(j - p[1])) * matrix[i][j]
                except KeyError:
                    my_map[matrix[i][j]] = (i, j)
    return -result


# Aynı olmayan sayıların birbirlerine olan uzaklıklarıyla sayıların farkının çarpımı döndürür
def dist_all(matrix):
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if (i != x or j != y) and matrix[i][j] != 0 and matrix[x][y] != 0 and matrix[x][y] != matrix[i][j]:
                        result += (abs(i - x) + abs(j - y)) * (abs(matrix[i][j] - matrix[x][y])) / 2
    return -result


# Boşluklarda çıkabilecek 2 ve 4 lere göre olasılık ağacını çıkaran fonksiyon
# Mevcut durumdan oluşabilecek bütün 2 ve 4'lerin eklenmiş halimin matrisini dönsürür
def odds(table):
    mat = table.copy()
    od = []
    for i in range(len(table)):
        for j in range(len(table[i])):
            if mat[i][j] == 0:
                mat[i][j] = 2
                buff = mat.copy()
                od.append(buff)
                mat[i][j] = 0
                mat[i][j] = 4
                od.append(mat)
                mat = table.copy()
    return od


# Tüm fitness fonksiyonlarının ağırlıklarıyla çarpının toplamı
def fitness(weights, mat):
    return weights[0] * empty_box(mat) + weights[1] * sum_box(mat) + weights[2] * dist_center(mat) + weights[
        3] * dist_equals(mat) + weights[3] * dist_all(mat) + weights[4]*dist_edge(mat)


# Çıkacak 2 ve 4'lere göre oluşacak durumların fitness fonksiyonlarının ortalamasını döndürür
def mean_odds(mat, weight=[1, 0.0001, 100, 1, 1, 10]):
    mean_psb = 0
    psb = odds(mat)
    for i in range(len(psb)):
        mean_psb += fitness(weight, psb[i]) / len(psb)
    return mean_psb


# Tüm yönleri deneyerek oluşacak matrislerden sonra çıkacak 2 ve 4'lere göre
# oluşan durumların fitness fonksiyonu sonuçlarını döndürür
def fit_ways(table):
    fits = []

    mat = table.copy()
    move(mat, "left")
    left = mat

    mat = table.copy()
    move(mat, "right")
    right = mat

    mat = table.copy()
    move(mat, "up")
    up = mat

    mat = table.copy()
    move(mat, "down")
    down = mat

    fits.append(mean_odds(left))
    fits.append(mean_odds(right))
    fits.append(mean_odds(up))
    fits.append(mean_odds(down))

    return fits


def moveAndCalc(board, way):
    move(board, way)
    return odds(board)


def dfs(board, limit=2):
    if not limit:
        return board

    boards = [[dfs(i, limit=limit - 1) for i in moveAndCalc(board, "left")],
              [dfs(i, limit=limit - 1) for i in moveAndCalc(board, "right")],
              [dfs(i, limit=limit - 1) for i in moveAndCalc(board, "up")],
              [dfs(i, limit=limit - 1) for i in moveAndCalc(board, "down")]]

    return boards


def best_way(table, seq):
    fits = fit_ways(table)
    ways = ["left", "right", "up", "down"]

    for i in range(len(fits)):
        for j in range(0, len(fits) - i - 1):
            if fits[j] < fits[j + 1]:
                fits[j], fits[j + 1] = fits[j + 1], fits[j]
                ways[j], ways[j + 1] = ways[j + 1], ways[j]
    return ways[seq]


# def train():
#     table = create_table(n)
#     print(table)
#     path = ["left", "right", "up", "down"]
#     while not is_end(table):
#         print(table)
#         # boards = dfs(table.copy(), 2)
#         # index = 0
#         # flag = False
#         # way = [0, 1, 2, 3]
#         # while not flag:
#         #     max = -999999
#         #     i = 0
#         #     while i < len(way):
#         #         for j in range(len(boards[way[i]])):
#         #             for k in range(len(boards[way[i]][j])):
#         #                 for t in range(len(boards[way[i]][j][k])):
#         #                     # print("1:",len(boards),"2:",len(boards[0]),"3:",len(boards[0][0]),"4:",len(boards[0][0][0]),"5:",len(boards[0][0][0][0]),"6:",len(boards[0][0][0][0][0]))
#         #                     # print(boards[way[i]][j][k][t])
#         #                     if (fitness([1, 1, 1, 2, 1], boards[way[i]][j][k][t])) > max:
#         #                         max = fitness([1, 1, 1, 2, 1], boards[way[i]][j][k][t])
#         #                         index = way[i]
#         #         print(i)
#         #         i += 1
#         #     print(way)
#         #     print(index)
#         #     way.pop(way.index(way[index]))
#         #
#         #
#         #     flag = move(table, path[index])
#
#         # print(path[index])
#         generate_number(table)

# El ile oyunu oynamak için bir fonksiyon
def game():
    table = create_table(4)
    print(table)

    while not is_end(table):
        way = str(msvcrt.getch())
        if way == "b'4'":
            flag = move(table, "left")
        elif way == "b'8'":
            flag = move(table, "up")
        elif way == "b'6'":
            flag = move(table, "right")
        elif way == "b'5'":
            flag = move(table, "down")
        else:
            flag = False
        if flag:
            generate_number(table)
            print("Empty Boxes:", empty_box(table))
            print("Sum of Boxes:", sum_box(table))
            print("Distance Center:", dist_center(table))
            print("Distance of Equals:", dist_equals(table))
            print("Distance of all: ", dist_all(table))
            print(table)


def train():
    table = create_table(4)
    print(table)
    while not is_end(table):
        way = best_way(table.copy(), 0)
        i = 1
        while not move(table, way) and i < 4:
            way = best_way(table.copy(), i)
            print(i)
            i += 1
        generate_number(table)
        move(table, way)
        print("Empty Boxes:", empty_box(table))
        print("Sum of Boxes:", sum_box(table))
        print("Distance Center:", dist_center(table))
        print("Distance of Equals:", dist_equals(table))
        print("Distance of all: ", dist_all(table))
        print(way)
        print(table)


train()
# game()
