from puissance4 import *
from Arbres_complet import Arbre
from copy import deepcopy
import time

score_2 = 50
score_3 = 200
score_4 = 1000


def arbre_possibles(arbre: Arbre, joueur: int, profondeur: int) -> Arbre:
    grille, colonne = arbre.get_valeur()
    if profondeur == 0:
        return arbre
    elif victoire(grille, int(not joueur)):
        return arbre
    else:
        for coup in coup_indice:
            grille_bis = deepcopy(grille)
            if coup_valide(coup, grille_bis):
                grille_bis = joue_coup(coup, grille_bis, joueur)
                enfant = Arbre((grille_bis, coup))
                enfant = arbre_possibles(
                    enfant, int(not joueur), profondeur - 1)
                arbre.ajouter_enfant(enfant)
        return arbre


def score_grille(grille: list, joueur: int) -> int:
    score = 0
    for i in range(hauteur):
        ligne = get_ligne(grille, i)
        for k in range(4):
            score += score_fenetre(ligne[k:k + 4], joueur)
    for i in range(largeur):
        colonne = get_colonne(grille, i)
        for k in range(3):
            score += score_fenetre(colonne[k:k + 4], joueur)
    i = 0
    for j in range(4):
        diagonale = get_diagonale(grille, i, j, 0)
        for k in range(len(diagonale) - 3):
            score += score_fenetre(diagonale[k:k + 4], joueur)
    for i in range(1, 3):
        diagonale = get_diagonale(grille, i, 0, 0)
        for k in range(len(diagonale) - 3):
            score += score_fenetre(diagonale[k:k + 4], joueur)
    i = 5
    for j in range(4):
        diagonale = get_diagonale(grille, i, j, 1)
        for k in range(len(diagonale) - 3):
            score += score_fenetre(diagonale[k:k + 4], joueur)
    for i in range(3, 6):
        diagonale = get_diagonale(grille, i, 0, 1)
        for k in range(len(diagonale) - 3):
            score += score_fenetre(diagonale[k:k + 4], joueur)
    return score


def score_fenetre(fenetre: list, joueur: int) -> int:
    """
    Fonction qui renvoie le score d'un joueur sur une fenêtre précise
    """
    nombres_joueur = fenetre.count(jetons[joueur])
    nombres_adversaire = fenetre.count(jetons[int(not joueur)])
    if nombres_joueur == 2 and nombres_adversaire == 0:
        return score_2
    elif nombres_joueur == 3 and nombres_adversaire == 0:
        return score_3
    elif nombres_joueur == 4:
        return score_4
    elif nombres_joueur == 0 and nombres_adversaire == 2:
        return -score_2
    elif nombres_joueur == 0 and nombres_adversaire == 3:
        return -score_3
    elif nombres_adversaire == 4:
        return -score_4
    else:
        return 0


def minimax(noeud: Arbre, maxi: bool, joueur: int) -> (int, str):
    """
    Calcule le score de ce nœud en tenant compte du fait que l’on cherche ou
    non à maximiser le score (indiqué par le booléen maxi)
    Renvoie ce score et la colonne
    """
    if noeud.est_feuille():
        grille, colonne = noeud.get_valeur()
        return (score_grille(grille, joueur), colonne)
    elif maxi:
        score = -float('inf')
        colonne = None
        for enfant in noeud.get_enfants():
            score, colonne = max((score, colonne),
                                 (minimax(enfant, False, joueur)[0], enfant.get_valeur()[1]))
        return score, colonne
    else:
        score = float('inf')
        colonne = None
        for enfant in noeud.get_enfants():
            score, colonne = min((score, colonne),
                                 (minimax(enfant, True, joueur)[0], enfant.get_valeur()[1]))
        return score, colonne
