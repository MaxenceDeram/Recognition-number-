from PIL import Image
import os

# ouverture d'une image
def load_image(path):
    """Ouvre une image depuis un chemin fichier."""
    img = Image.open(path)
    return img

# conversion en niveaux de gris
def to_grayscale(img):
    """Convertit l'image en niveaux de gris."""
    return img.convert("L")

# binarisation de l'image
def binarize(img, threshold=128):
    """
    Convertit l'image en noir et blanc (0 ou 1)
    selon un seuil.
    """
    pixels = img.load()
    width, height = img.size
    binary = []

    for y in range(height):
        row = []
        for x in range(width):
            if pixels[x, y] > threshold:
                row.append(1)  # blanc
            else:
                row.append(0)  # noir
        binary.append(row)

    return binary

# redimensionnement de l'image
def normalize_size(img, size=(10, 10)):
    """Redimensionne l'image à une taille standard (10x10 par défaut)."""
    return img.resize(size)

# conversion de l'image en matrice de pixels
def to_matrix(img):
    """Convertit l'image en matrice de pixels (liste de listes)."""
    pixels = img.load()
    width, height = img.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(pixels[x, y])
        matrix.append(row)

    return matrix

def matrix_to_vector(matrix):
    """Aplatit une matrice en un vecteur 1D."""
    vector = []
    for row in matrix:
        for pixel in row:
            vector.append(pixel)
    return vector

# construction de la base de données
def build_dataset(folder):
    """
    Charge les images de référence (1.png à 9.png) depuis un dossier
    et retourne un dictionnaire { chiffre : vecteur binaire }.
    """
    dataset = {}

    for digit in range(1, 9):
        path = os.path.join(folder, f"{digit}.png")
        if not os.path.exists(path):
            print(f"[ATTENTION] Image manquante : {path}")
            continue

        img = load_image(path)
        img = to_grayscale(img)
        img = normalize_size(img)
        matrix = to_matrix(img)
        binary = binarize(img)
        vector = matrix_to_vector(binary)
        dataset[digit] = vector

    return dataset


# comparaison de vecteurs
def distance(v1, v2):
    """Calcule le nombre de pixels différents entre deux vecteurs."""
    diff = 0
    for a, b in zip(v1, v2):
        if a != b:
            diff += 1
    return diff

def recognize(image_path, dataset):
    """
    Compare le vecteur de l'image cible avec la base de données
    et retourne le chiffre le plus proche.
    """
    img = load_image(image_path)
    img = to_grayscale(img)
    img = normalize_size(img)
    binary = binarize(img)
    vector = matrix_to_vector(binary)

    best_digit = None
    best_score = float("inf")

    for digit, ref_vector in dataset.items():
        score = distance(vector, ref_vector)
        if score < best_score:
            best_score = score
            best_digit = digit

    return best_digit, best_score

# réception de l'image cible et affichage du résultat
def main():
    print("=== Reconnaissance de chiffres ===\n")

    # Dossier contenant les images de référence (là où se trouve ce script)
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Image")

    # chargement de la base de données
    print("Chargement de la base de données...")
    dataset = build_dataset(folder)
    print(f"{len(dataset)} chiffres chargés.\n")

    while True:
        path = input("Entrez le chemin de votre image (ou 'q' pour quitter) : ").strip()

        if path.lower() == 'q':
            print("Au revoir !")
            break

        try:
            digit, score = recognize(path, dataset)

            # Affichage visuel de votre image
            img = load_image(path)
            img = to_grayscale(img)
            img = normalize_size(img)
            binary = binarize(img)

            print("\n── Votre image ──")
            for row in binary:
                print(" ".join("0" if p == 0 else "1" for p in row))

            # Affichage de la matrice de référence
            ref_path = os.path.join(folder, f"{digit}.png")
            ref_img = load_image(ref_path)
            ref_img = to_grayscale(ref_img)
            ref_img = normalize_size(ref_img)
            ref_binary = binarize(ref_img)

            print(f"\n── Référence (chiffre {digit}) ──")
            for row in ref_binary:
                print(" ".join("0" if p == 0 else "1" for p in row))

            print(f"\n➜  Chiffre reconnu : {digit}  (score de différence : {score} pixels)\n")

        except FileNotFoundError:
            print(f"[ERREUR] Fichier introuvable : {path}\n")
        except Exception as e:
            print(f"[ERREUR] {e}\n")


if __name__ == "__main__":  # point d'entrée du script
    main()