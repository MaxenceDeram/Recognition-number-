from image_processing import *
from dataset import dataset

def distance(v1, v2):
    d = 0
    for i in range(len(v1)):
        d += abs(v1[i] - v2[i])
    return d

def predict(vector):
    best_digit = None
    best_score = 999999

    for digit in dataset:
        d = distance(vector, dataset[digit])
        if d < best_score:
            best_score = d
            best_digit = digit

    return best_digit

matrix = image_to_matrix("eight.jpg")
binary = binarize(matrix)
vector = matrix_to_vector(binary)
digit = predict(vector)
print("Predicted digit:", digit)
