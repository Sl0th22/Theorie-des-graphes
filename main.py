from collections import deque
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


def VerifCircuit(data):
    lines = data.strip().split('\n')
    mat = []
    durees = {}

    for line in lines:
        elements = [int(x) for x in line.strip().split()]
        sommet = elements[0]
        duree = elements[1]
        predecesseurs = elements[2:]
        mat.append((sommet, duree, predecesseurs))
        durees[sommet] = duree

    # Étape 2 : Initialiser les degrés d'entrée
    sommets = set(durees.keys())
    degres_entree = {}
    for s in sommets:
        degres_entree[s] = 0

    for tache in mat:
        for pred in tache[2]:  # prédécesseurs
            degres_entree[tache[0]] += 1

    # Étape 3 : suppression des points d'entrée
    reste = set(sommets)
    print("Début de la détection de circuit :")

    while True:
        # Chercher les sommets avec degré d'entrée 0
        points_entree = []
        for s in reste:
            if degres_entree[s] == 0:
                points_entree.append(s)

        if not points_entree:
            break  # Aucun point d'entrée → cycle possible
        print(f"Points d’entrée : {points_entree}")

        for s in points_entree:
            reste.remove(s)
            # Supprimer s des listes de prédécesseurs des autres tâches
            for tache in mat:
                if s in tache[2]:
                    tache[2].remove(s)
                    degres_entree[tache[0]] -= 1

    # Étape 4 : Conclusion
    if reste:
        print("Circuit détecté ! Sommets restants bloqués :", reste)
        return False
    else:
        print("Aucun circuit détecté. Le graphe est valide pour l’ordonnancement.")
        return True


def ArcValeurNegative(data):
    lines = data.strip().split('\n')
    for line in lines:
        elements = [int(x) for x in line.strip().split()]
        duree = elements[1]
        if duree < 0:
            print("Arc negatif")
            return False

    print("Arc positif")
    return True

def succduree(mat):
    nb_sommets = max(item[0] for item in mat) + 1
    duree2 = [0] * nb_sommets
    successeurs = [[] for _ in range(nb_sommets)]
    for sommet, duree, _ in mat:
        duree2[sommet] = duree
    for sommet, _, predecesseurs in mat:
        for pred in predecesseurs:
            successeurs[pred].append(sommet)

    return duree2, successeurs

def tri_topologique(mat):
    nb_sommets = max(tache[0] for tache in mat) + 1
    degres_entree = [0] * nb_sommets
    succ = [[] for _ in range(nb_sommets)]
    rangs = [-1] * nb_sommets

    for sommet, _, predecesseurs in mat:
        for pred in predecesseurs:
            degres_entree[sommet] += 1
            succ[pred].append(sommet)
    temp = deque()

    for i in range(nb_sommets):
        if degres_entree[i] == 0:
            temp.append(i)
            rangs[i] = 0
    ordre_topologique = []

    while temp:
        j = temp.popleft()
        ordre_topologique.append(j)
        for k in succ[j]:
            degres_entree[k] -= 1
            if degres_entree[k] == 0:
                rangs[k] = rangs[j] + 1
                temp.append(k)
    if -1 in rangs:
        print("Le graphe contient un cycle donc le tri topologique impossible.")
        return None

    print("\n Rangs des sommets :")
    for i in range(nb_sommets):
        print(f"Sommet {i} : rang = {rangs[i]}")

    print("\n Ordre topologique :")
    print(ordre_topologique)

    return ordre_topologique

def calendrier_plus_tot(duree2, succ,topo):
    a = len(duree2)
    tot = [0] * a

    for i in topo:
        for j in succ[i]:
            tot[j] = max(tot[j], tot[i] + duree2[i])

    print("\nTOT")
    print("Tâche | plus tôt")
    print("------------------")
    for i in range(a):
        print(f"{i:5} | {tot[i]:9}")

    return tot

def calendrier_plus_tard(duree2, succ, topo, tot):
    a = len(duree2)
    duree = max(tot) 
    tard = [duree] * a

    for i in reversed(topo):
        for j in succ[i]:
            tard[i] = min(tard[i], tard[j] - duree2[i])
    
    print("\nTARD")
    print("Tâche | plus tard")
    print("------------------")
    for i in range(a):
        print(f"{i:5} | {tard[i]:9}")
    
    return tard

data = loadficher()
mat = AjoutAlphaOmega(data)
#afficherSimple(data)
#afficherMatrice(mat)
#ArcValeurNegative(data)
#VerifCircuit(data)
succduree(mat)
duree2, succ = succduree(mat)
tri_topologique(mat)
topo = tri_topologique(mat)
tot=calendrier_plus_tot(duree2, succ,topo)
tard = calendrier_plus_tard(duree2, succ, topo, tot)