import numpy as np
import random

n = 4  # matrix lenght


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


def generate_number(mat):
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


def move(mat, way):
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
            if write == True:
                mat[i][:] = buffer
    # elif way == "up":
    #     prop(mat, up)
    # elif way == "down":
    #     prob(mat, "down")
    elif way == "right":
        for i in range(len(mat)):
            index = len(mat)-1
            cursor = mat[i][index]
            j = len(mat)-2
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
            t = len(mat)-1
            buffer = [0] * len(mat)
            for k in range(len(mat[i])-1,-1,-1):
                if mat[i][k] != 0:
                    write = True
                    buffer[t] = mat[i][k]
                    t -= 1
            if write == True:
                mat[i][:] = buffer
    else:
        print("Way Error!")

table = create_table(n)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
generate_number(table)
print("Generate Number")
print(table)



move(table, "right")
print(table)
move(table, "left")
print(table)
