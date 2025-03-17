with open('table 3.txt', 'r', encoding='utf-8') as fichier:
    data = fichier.read()

# Analyse des données
lines = data.strip().split('\n')
mat = []

# Conversion des lignes en listes d'entiers
for line in lines:
    mat.append([int(x) for x in line.strip().split()])

# Trouver la longueur maximale des lignes
max_len = max(len(line) for line in mat)

# Compléter les lignes avec des 0 si nécessaire
for i in range(len(mat)):
    while len(mat[i]) < max_len:
        mat[i].append(0)

# Affichage de la matrice ajustée
print(mat)
