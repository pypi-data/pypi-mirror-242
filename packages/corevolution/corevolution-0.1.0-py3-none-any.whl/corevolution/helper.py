

def convert_array_to_matrix(array_1, n: int, m: int) -> list[list]:
    matrix = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = array_1[i + j * m]

    return matrix

