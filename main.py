def loadficher():
    print("Quel table voulez-vous afficher ? Donnez un nombre entre 1 et 14")
    nb = input()
    while not nb.isdigit() or int(nb) < 1 or int(nb) > 14:
        print("Veuillez entrer un nombre entre 1 et 14")
        nb = input()

    with open('table ' + nb + '.txt', 'r', encoding='utf-8') as fichier:
        data = fichier.read()
    return data

def AjoutAlphaOmega(data):
    lines = data.strip().split('\n')
    mat = []
    durees = {}
    sommets = set()

    # Stocker les durées, les sommets et les prédécesseurs
    for line in lines:
        elements = [int(x) for x in line.strip().split()]
        sommet = elements[0]
        duree = elements[1]
        predecesseurs = elements[2:]
        mat.append([sommet, duree, predecesseurs])  # Remplacer le tuple par une liste
        durees[sommet] = duree
        sommets.add(sommet)
        sommets.update(predecesseurs)

    # Ajouter alpha (0) et omega (N+1) au graphe
    N = len(sommets)
    alpha = 0
    omega = N + 1

    # Trouver les racines initiales (sommet sans prédécesseur)
    racines = [sommet for sommet, _, predecesseurs in mat if not predecesseurs]

    # Trouver les sommets sans successeurs (qui ne figurent pas dans les prédécesseurs d'autres sommets)
    sommets_avec_successeurs = set(sommet for _, _, predecesseurs in mat for sommet in predecesseurs)
    sans_successeurs = [sommet for sommet, _, _ in mat if sommet not in sommets_avec_successeurs]

    # Ajouter alpha (0) sans prédécesseur mais comme prédécesseur des racines initiales
    for racine in racines:
        for item in mat:
            if item[0] == racine:
                item[2].insert(0, alpha)  # Ajouter alpha (0) comme prédécesseur
    mat.append([alpha, 0, []])
    # Ajouter omega (N+1) avec tous les sommets sans successeurs comme prédécesseurs
    if sans_successeurs:
        mat.append([omega, 0, sans_successeurs])  # Omega (N+1) comme prédécesseur des sommets sans successeurs

    # Affichage de la matrice résultante
    print(mat)
    return mat




def afficherSimple(data):
    # Analyse des données
    lines = data.strip().split('\n')
    mat = []
    durees = {}
    liens = []

    # Stocker les durées pour chaque sommet
    for line in lines:
        elements = [int(x) for x in line.strip().split()]
        sommet = elements[0]
        duree = elements[1]
        predecesseurs = elements[2:]
        mat.append((sommet, duree, predecesseurs))
        durees[sommet] = duree

    # Stocker les liens avec la durée du prédécesseur
    for sommet, _, predecesseurs in mat:
        for pred in predecesseurs:
            pred_duree = durees.get(pred, 0)  # Durée du prédécesseur
            liens.append((pred, sommet, pred_duree))

    # Trier les liens par prédécesseur (ordre croissant)
    liens.sort(key=lambda x: x[0])

    # Afficher les liens triés
    for pred, sommet, duree in liens:
        print(f"{pred} -> {sommet} : {duree}")



def afficherMatrice(data):
    # Analyse des données
    mat = []
    durees = {}
    sommets = set()

    # Stocker les durées et les sommets
    for sommet, duree, predecesseurs in data:
        mat.append((sommet, duree, predecesseurs))
        durees[sommet] = duree
        sommets.add(sommet)
        sommets.update(predecesseurs)

    # Trier les sommets et les mapper aux indices continus
    sommets = sorted(sommets)
    sommet_index = {sommets[i]: i for i in range(len(sommets))}

    # Initialiser la matrice carrée
    taille = len(sommets)
    matrice = [['*' for i in range(taille)] for i in range(taille)]

    # Remplir la matrice avec les durées des prédécesseurs
    for sommet, duree, predecesseurs in mat:
        for pred in predecesseurs:
            # Mappage des sommets aux indices dans la matrice
            i = sommet_index.get(sommet)
            j = sommet_index.get(pred)
            if i is not None and j is not None:
                matrice[j][i] = durees.get(pred, '-')

    # Affichage des en-têtes horizontaux
    print("     ", end="")
    for s in sommets:
        print(f"{s:>2}", end=" ")
    print()

    # Affichage de la ligne horizontale
    print("    " + "---" * len(sommets))

    # Affichage des lignes de la matrice
    for i, s in enumerate(sommets):
        print(f"{s:>2} |", end=" ")  # Afficher le sommet avec la ligne verticale
        for j in range(len(sommets)):
            print(f"{matrice[i][j]:>2}", end=" ")
        print()

    # Affichage de la ligne horizontale en bas
    print("    " + "---" * len(sommets))



data = loadficher()
mat = AjoutAlphaOmega(data)
afficherSimple(data)
afficherMatrice(mat)