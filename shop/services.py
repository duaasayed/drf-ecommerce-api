import numpy as np


def calc_cosine_similarity(v1, v2):
    dot_product = calc_dot_product(v1, v2)
    v1_euclidean_norm = calc_euclidean_norm(v1)
    v2_euclidean_norm = calc_euclidean_norm(v2)

    cosine_similarity = dot_product / (v1_euclidean_norm * v2_euclidean_norm)
    return cosine_similarity


def calc_dot_product(v1, v2):
    return np.dot(np.array(v1), np.array(v2))


def calc_euclidean_norm(v):
    return np.linalg.norm(np.array(v))
