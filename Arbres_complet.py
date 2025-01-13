import graphviz
from pilesFiles import Pile, File


class Arbre:
    """
    Classe implémentant un arbre dont les noeuds sont caractérisés par 
    - une valeur (de type quelconque)
    - des enfants
    Les enfants sont stockés dans une liste (vide apr défaut) et sont eux-mêmes des arbres
    """

    def __init__(self, valeur=None, enfants=None):
        """
        Constructeur
        """
        if valeur:
            self.valeur = valeur
            if enfants:
                self.enfants = enfants
            else:
                self.enfants = []
        else:  # arbre vide
            self.valeur = None
            self.enfants = []

    def get_valeur(self):
        """
        Accesseur de la valeur de l'arbre
        """
        return self.valeur

    def set_valeur(self, valeur):
        """
        Mutateur de la valeur de l'arbre
        """
        self.valeur = valeur

    def get_enfants(self):
        """
        Accesseur des enfants
        """
        return self.enfants

    def ajouter_enfant(self, enfant):
        """
        Ajoute l'enfant aux enfants de cet arbre
        """
        assert isinstance(enfant, Arbre), "L'enfant doit être un arbre"

        self.enfants.append(enfant)

    def sous_arbre(self, valeur_enfant):
        """
        Retourne le sous-arbre correspondant à l'enfant (désigné par sa valeur) et passé en argument
        Renvoie None si le nœud n'existe pas
        """
        pile = Pile()

        pile.empiler(self)

        while not pile.est_vide():
            enCours = pile.depiler()
            if enCours.get_valeur() == valeur_enfant:
                return enCours
            else:
                for e in enCours.get_enfants():
                    pile.empiler(e)

        return None

    def est_feuille(self) -> bool:
        """
        Renvoie True si l'arbre est une feuille (pas d'enfants)
        False dans le cas contraire
        """
        return len(self.enfants) == 0

    def retirer_enfant(self, valeur_enfant) -> None:
        """
        Retire l'enfant de la liste des enfants de cet arbre
        Lève une erreur si l'enfant n'est pas dans la liste des enfants
        """
        if not self.sous_arbre(valeur_enfant):
            raise Exception("L'enfant n'est pas dans les enfants de cet arbre")
        else:
            i = 0
            for enfant in self.enfants:
                if enfant.get_valeur() == valeur_enfant:
                    self.enfants.pop(i)
                    break
                else:
                    i += 1

    def hauteur_iterative(self) -> int:
        """
        Renvoie la hauteur de l'arbre
        Renvoie 1 si l'arbre est une feuille
        """
        h = 0
        if self.get_valeur():
            h += 1

        pile = Pile()

        pile.empiler((self, h))

        while not pile.est_vide():
            enCours, niveau = pile.depiler()
            h = max(h, niveau)
            for enfant in enCours.get_enfants():
                pile.empiler((enfant, niveau + 1))

        return h

    def hauteur_recursive(self) -> int:
        """
        Renvoie la hauteur de l'arbre
        Renvoie 1 si l'arbre est une feuille
        """
        h = 1

        hauteurs = [0]

        for enfant in self.enfants:
            hauteurs.append(enfant.hauteur_recursive())

        return h + max(hauteurs)

    def taille(self) -> int:
        """
        Renvoie la taille de l'arbre (le nombre de nœud)
        """
        t = 0
        if self.get_valeur():
            t += 1

        for enfant in self.get_enfants():
            t += enfant.taille()

        return t

    def parcours_largeur(self) -> str:
        """
        Renvoie la chaîne de caractère formée par les valeurs
        des nœuds rencontrés lors d'un parcours en largeur
        """
        if self.valeur is None:
            return "L'arbre est vide"

        p = ""

        f = File()

        f.enfiler(self)

        while not f.est_vide():
            enCours = f.defiler()
            p += (enCours.get_valeur() + " -> ")
            for enfant in enCours.get_enfants():
                f.enfiler(enfant)

        return p[:-4]

    def parcours_profondeur_prefixe(self, depart=True) -> str:
        """
        Renvoie la chaîne de caractère formée par les valeurs
        des nœuds rencontrés lors d'un parcours en profondeur prefixe
        """
        if self.valeur is None:
            return "L'arbre est vide"

        p = self.valeur + " -> "

        for enfant in self.enfants:
            if enfant:
                p += enfant.parcours_profondeur_prefixe(False)

        if depart:
            return p[:-4]
        else:
            return p

    def parcours_profondeur_postfixe(self, depart=True) -> str:
        """
        Renvoie la chaîne de caractère formée par les valeurs
        des nœuds rencontrés lors d'un parcours en profondeur postfixe
        """
        if self.valeur is None:
            print("L'arbre est vide")
            return ""

        p = ""

        for enfant in self.enfants:
            p += enfant.parcours_profondeur_postfixe(False)

        p += self.valeur + " -> "

        if depart:
            return p[:-4]
        else:
            return p

    def __str__(self):
        """
        Représentationd dee l'arbre dans la console
        """
        h_barre = "_____"

        s = ""
        if self.valeur is None:
            s = "L'arbre est vide"
        else:
            depth = 0
            p = Pile()
            p.empiler((self, depth))
            while not p.est_vide():
                enCours, depth = p.depiler()
                if depth > 0:
                    s += "  |" + (" " * 8 + "|") * (depth - 1) + h_barre + str(enCours.get_valeur()) + "\n"
                elif depth == 0:
                    s += str(enCours.get_valeur()) + "\n"

                for enfant in enCours.get_enfants():
                    p.empiler((enfant, depth + 1))

        return s


if __name__ == "__main__":
    s7 = Arbre("Noeud 7")
    s6 = Arbre("Noeud 6")
    s5 = Arbre("Noeud 5")
    s4 = Arbre("Noeud 4", [s5, s6])
    s3 = Arbre("Noeud 3", [s4])
    s2 = Arbre("Noeud 2", [s7])
    arbre = Arbre("Noeud 1")
    arbre.ajouter_enfant(s3)
    arbre.ajouter_enfant(s2)

    print(f"Hauteur de l'arbre : {arbre.hauteur_iterative()}")
    print(f"Hauteur (récursive) de l'arbre : {arbre.hauteur_recursive()}")
    print(f"Taille de l'arbre : {arbre.taille()}")
    print(f"Taille de l'arbre : {arbre.taille()}")
    print(f"Parcours en largeur de l'arbre : {arbre.parcours_largeur()}")
    print(
        f"Parcours en profondeur prefixe de l'arbre : {arbre.parcours_profondeur_prefixe()}")
    print(
        f"Parcours en profondeur postfixe de l'arbre : {arbre.parcours_profondeur_postfixe()}")

    print(
        f"Hauteur de l'arbre 'Noeud 4' : {arbre.sous_arbre('Noeud 4').hauteur_iterative()}")
    print(
        f"Hauteur (récursive) de l'arbre 'Noeud 4' : {arbre.sous_arbre('Noeud 4').hauteur_recursive()}")
    print(
        f"Taille de l'arbre 'Noeud 4' : {arbre.sous_arbre('Noeud 4').taille()}")

    print(arbre)
