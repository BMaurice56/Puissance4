from time import sleep
import os
# création de la grille de jeux
grille = [
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "."]
]

largeur = len(grille[0])
hauteur = len(grille)

# création du joueur 0 et 1
joueur = 0
# création du jeton attribué au joueur
jetons = {0: "O", 1: "X"}

coup_indice = {"a": 0,
               "b": 1,
               "c": 2,
               "d": 3,
               "e": 4,
               "f": 5,
               "g": 6}
indice_coup = {v: k for k, v in coup_indice.items()}


def affichage(grille: list) -> None:
    print("  a   b   c   d   e   f   g")
    for ligne in range(hauteur):
        print("| ", end="")
        for colonne in range(largeur):
            print(grille[ligne][colonne], end="")
            print(" | ", end="")
        print()

def affichage_str(grille: list) -> str:
    resultat = "  a   b   c   d   e   f   g\n"

    for ligne in range(hauteur):
        resultat += "| "
        for colonne in range(largeur):
            resultat += grille[ligne][colonne] + " | "
        resultat += "\n"

    return resultat

def get_ligne(grille: list, i: int) -> list:
    """
    Renvoie la ligne i de la grille
    """
    if i > len(grille) - 1 or i < 0:
        raise Exception("La ligne rechercher n'est pas dans la grille")
    return grille[i]


def get_colonne(grille: list, i: int) -> list:
    """
    Renvoie la colonne i de la grille
    """
    colonne = []
    if i > len(grille) or i < 0:
        raise Exception("La colonne rechercher n'est pas dans la grille")
    for j in range(len(grille)):
        colonne.append(grille[j][i])
    return colonne


def get_diagonale(grille, i, j, direction):
    diagonale = []
    if direction == 0:
        while i < hauteur and j < largeur:
            diagonale.append(grille[i][j])
            i += 1
            j += 1
    else:
        while i >= 0 and j < largeur:
            diagonale.append(grille[i][j])
            i -= 1
            j += 1
    return diagonale


def victoire(grille: list, joueur: int) -> bool:
    """
    Cherche dans la grille si le joueur a gagné
    Renvoie True ou False selon la réponse
    """
    for i in range(hauteur):
        ligne = get_ligne(grille, i)
        for k in range(4):
            if ligne[k] == jetons[joueur] and ligne[k+1] == jetons[joueur] and ligne[k+2] == jetons[joueur] and ligne[k+3] == jetons[joueur]:
                return True
    for i in range(largeur):
        colonne = get_colonne(grille, i)
        for k in range(3):
            if colonne[k] == jetons[joueur] and colonne[k+1] == jetons[joueur] and colonne[k+2] == jetons[joueur] and colonne[k+3] == jetons[joueur]:
                return True
    i = 0
    for j in range(4):
        diagonale = get_diagonale(grille, i, j, 0)
        for k in range(len(diagonale)-3):
            if diagonale[k] == jetons[joueur] and diagonale[k+1] == jetons[joueur] and diagonale[k+2] == jetons[joueur] and diagonale[k+3] == jetons[joueur]:
                return True

    for i in range(1, 3):
        diagonale = get_diagonale(grille, i, 0, 0)
        for k in range(len(diagonale)-3):
            if diagonale[k] == jetons[joueur] and diagonale[k+1] == jetons[joueur] and diagonale[k+2] == jetons[joueur] and diagonale[k+3] == jetons[joueur]:
                return True
    i = 5
    for j in range(4):
        diagonale = get_diagonale(grille, i, j, 1)
        for k in range(len(diagonale)-3):
            if diagonale[k] == jetons[joueur] and diagonale[k+1] == jetons[joueur] and diagonale[k+2] == jetons[joueur] and diagonale[k+3] == jetons[joueur]:
                return True

    for i in range(3, 6):
        diagonale = get_diagonale(grille, i, 0, 1)
        for k in range(len(diagonale)-3):
            if diagonale[k] == jetons[joueur] and diagonale[k+1] == jetons[joueur] and diagonale[k+2] == jetons[joueur] and diagonale[k+3] == jetons[joueur]:
                return True
    return False


def coup_valide(coup: str, grille: list) -> bool:
    """
    Détermine si le coup proposé par le joueur est valide ou non
    """
    if coup not in ["a", "b", "c", "d", "e", "f", "g"]:
        print(" /!\ Coup non valide /!\ ")
        return False
    else:
        indice = coup_indice[coup]
        if get_colonne(grille, indice)[0] == ".":
            return True
        else:
            return False


def joue_coup(coup: str, grille: list, joueur: int) -> list:
    """
    Joue le coup donnée et renvoie la grille correspondante
    """
    colonne = coup_indice[coup]
    ligne = 0
    while ligne < hauteur-1 and grille[ligne+1][colonne] == ".":
        ligne = ligne + 1
    grille[ligne][colonne] = jetons[joueur]
    return grille
