import re
from collections import defaultdict

class Officine:
    def __init__(self, ingredients, recettes):
        self.stocks = defaultdict(int)
        self.ingredients = ingredients
        self.recettes = recettes
        self.alias = self._generer_alias()

    def _generer_alias(self):
        alias = {}

        # Gérer les ingrédients
        for ing in self.ingredients:
            parts = ing.split("/")
            if len(parts) == 2:  # ex : œil/yeux de grenouille
                sing, plur = parts
                nom_base = plur.split()[-1]
                sing_name = f"{sing} {nom_base}"
                plur_name = f"{plur} {nom_base}"
                alias[sing_name] = sing_name
                alias[plur_name] = sing_name
            else:
                alias[ing] = ing
                if not ing.endswith("s"):
                    alias[ing + "s"] = ing

        # Gérer les potions (ex: "fiole de glaires purulentes" → "fioles de glaires purulentes")
        for potion in self.recettes:
            alias[potion] = potion
            mots = potion.split()
            if len(mots) > 1 and not mots[0].endswith("s"):
                pluriel = " ".join([mots[0] + "s"] + mots[1:])
                alias[pluriel] = potion

        return alias

    def _normaliser_nom(self, nom):
        nom = nom.strip().lower()
        return self.alias.get(nom, nom)

    def rentrer(self, texte):
        match = re.match(r"(\d+)\s+(.+)", texte.strip())
        if not match:
            raise ValueError("Format invalide. Exemple attendu : '3 yeux de grenouille'")
        qte, nom = int(match.group(1)), self._normaliser_nom(match.group(2))
        self.stocks[nom] += qte

    def quantite(self, nom):
        nom = self._normaliser_nom(nom)
        return self.stocks[nom]

    def _analyser_recette(self, nom_potion):
        recette = self.recettes.get(nom_potion)
        if not recette:
            raise ValueError(f"Aucune recette connue pour {nom_potion}")
        resultats = []
        for ligne in recette:
            match = re.match(r"(\d+)\s+(.+)", ligne.strip())
            if not match:
                continue
            qte = int(match.group(1))
            nom_ing = self._normaliser_nom(match.group(2))
            resultats.append((nom_ing, qte))
        return resultats

    def preparer(self, texte):
        match = re.match(r"(\d+)\s+(.+)", texte.strip())
        if not match:
            raise ValueError("Format invalide. Exemple attendu : '2 fioles de glaires purulentes'")
        nb_voulues, nom_potion = int(match.group(1)), self._normaliser_nom(match.group(2))

        if nom_potion not in self.recettes:
            raise ValueError(f"Recette inconnue : {nom_potion}")

        recette = self._analyser_recette(nom_potion)

        # Calcul du nombre maximum possible selon les stocks
        max_possible = nb_voulues
        for ing, qte in recette:
            if self.stocks[ing] == 0:
                max_possible = 0
                break
            max_possible = min(max_possible, self.stocks[ing] // qte)

        if max_possible == 0:
            return 0

        # Mise à jour des stocks
        for ing, qte in recette:
            self.stocks[ing] -= qte * max_possible

        self.stocks[nom_potion] += max_possible
        return max_possible


# ingredients = [
#     "œil/yeux de grenouille",
#     "larme de brume funèbre",
#     "radicelle de racine hurlante",
#     "pincée de poudre de lune",
#     "croc de troll",
#     "fragment d'écaille de dragonnet",
#     "goutte de sang de citrouille"
# ]
# recettes = {
#     "fiole de glaires purulentes"   : [ "2 larmes de brume funèbre",  "1 goutte de sang de citrouille" ],
#     "bille d'âme évanescente"       : [ "3 pincées de poudre de lune", "1 œil de grenouille" ],
#     "soupçon de sels suffocants"    : [ "2 crocs de troll", "1 fragment d'écaille de dragonnet", "1 radicelle de racine hurlante" ],
#     "baton de pâte sépulcrale"      : [ "3 radicelles de racine hurlante", "1 fiole de glaires purulentes" ],
#     "bouffée d'essence de cauchemar": [ "2 pincées de poudre de lune", "2 larmes de brume funèbre" ]
# }

# o = Officine(ingredients, recettes)

# o.rentrer("3 yeux de grenouille")
# o.rentrer("4 larmes de brume funèbre")
# o.rentrer("2 gouttes de sang de citrouille")

# print(o.quantite("œil de grenouille"))  # 3
# print(o.preparer("2 fioles de glaires purulentes"))  # 2 préparées
# print(o.quantite("fiole de glaires purulentes"))  # 2
