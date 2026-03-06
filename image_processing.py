from PIL import Image

def image_to_matrix(path):

    img = Image.open(path)
    img = img.convert("L")

    pixels = img.load()
    width, height = img.size

    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(pixels[x, y])
        matrix.append(row)

    return matrix


def binarize(matrix, threshold=128):

    binary = []

    for row in matrix:
        new_row = []
        for pixel in row:
            if pixel > threshold:
                new_row.append(1)
            else:
                new_row.append(0)
        binary.append(new_row)

    return binary


def matrix_to_vector(matrix):

    vector = []

    for row in matrix:
        for pixel in row:
            vector.append(pixel)

    return vector