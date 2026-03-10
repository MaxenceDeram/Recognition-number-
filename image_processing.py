from PIL import Image
import os

def transformer_image(path):
    # Ouvre l'image, la met en gris, la redimensionne en 10x10
    img = Image.open(path)
    img = img.convert("L")
    img = img.resize((10, 10))

    # Transforme l'image en matrice binaire puis en vecteur
    pixels = img.load()
    vecteur = []

    for y in range(10):
        for x in range(10):
            if pixels[x, y] > 128:
                vecteur.append(1)
            else:
                vecteur.append(0)

    return vecteur

def construire_base(folder):
    base = {}

    for chiffre in range(1, 10):   # de 1 à 9
        path = os.path.join(folder, f"{chiffre}.png")

        if os.path.exists(path):
            base[chiffre] = transformer_image(path)
        else:
            print(f"Image manquante : {path}")

    return base
# Calcule la distance entre deux vecteurs (nombre de pixels différents)
def calculer_distance(v1, v2):
    diff = 0

    for i in range(len(v1)):
        if v1[i] != v2[i]:
            diff += 1

    return diff

def reconnaitre_chiffre(image_path, base):
    vecteur_test = transformer_image(image_path)

    meilleur_chiffre = None
    meilleure_distance = 1000000 

    for chiffre in base:
        dist = calculer_distance(vecteur_test, base[chiffre])

        if dist < meilleure_distance:
            meilleure_distance = dist
            meilleur_chiffre = chiffre

    return meilleur_chiffre, meilleure_distance

def afficher_image_binaire(path):
    img = Image.open(path)
    img = img.convert("L")
    img = img.resize((10, 10))

    pixels = img.load()

    for y in range(10):
        ligne = []
        for x in range(10):
            if pixels[x, y] > 128:
                ligne.append("1")
            else:
                ligne.append("0")
        print(" ".join(ligne))

def main():
    print("=== Reconnaissance de chiffres ===")

    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Image")

    print("Chargement des références...")
    base = construire_base(dossier)
    print(f"{len(base)} chiffres chargés.\n")

    while True:
        chemin = input("Chemin de l'image à tester (ou q pour quitter) : ")

        if chemin.lower() == "q":
            print("Au revoir !")
            break

        try:
            chiffre, score = reconnaitre_chiffre(chemin, base)

            print("\n--- Votre image ---")
            afficher_image_binaire(chemin)

            ref_path = os.path.join(dossier, f"{chiffre}.png")
            print(f"\n--- Référence : {chiffre} ---")
            afficher_image_binaire(ref_path)

            print(f"\nChiffre reconnu : {chiffre}")
            print(f"Différence : {score} pixels\n")
        
        except Exception as e:
            print(f"Erreur : {e}\n")

if __name__ == "__main__":
    main()