import csv
from api_neo4j import API

with open('logs.txt', 'r', encoding='utf-8') as fichier:
    for ligne in fichier:
        mdp = ligne
        
api = API(mdp)

# Lecture du fichier csv : 
filepath = "data/communes-departement-region.csv"
# Lire les 1000 premières lignes
with open(filepath, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Lire l'en-tête
    rows = [row for _, row in zip(range(1000), reader)] 

noms_regions = []
lien_departements_regions = {}
lien_communes_departements = {}
noms=set()

for row in rows:
    # Ajouter des informations dans lien_communes_departements
    if row[14] not in lien_communes_departements:
        lien_communes_departements[row[12]] = [row[9]]  # Initialiser avec une liste contenant les données
    else:
        lien_communes_departements[row[12]].append([row[9]])  # Ajouter à la liste existante

    # Ajouter des noms de régions
    if row[14] not in noms_regions:
        noms_regions.append(str(row[14]))

    # Ajouter des informations dans lien_departements_regions
    if row[14] not in lien_departements_regions:
        lien_departements_regions[row[14]] = [row[12]]  # Initialiser avec une liste contenant row[12]
    elif row[12] not in lien_departements_regions[row[14]]:
        lien_departements_regions[row[14]].append(row[12])  # Ajouter row[12] si elle n'est pas déjà présente
    
    noms.add(row[14])
    noms.add(row[12])
    noms.add(row[9])
        
#print(noms_regions)
print(lien_departements_regions)
print(lien_communes_departements)

api.createTable("communes", noms)
''''
api.setLiens(lien_departements_regions, 'contient')
api.setLiens(lien_communes_departements, 'contient')'''
#all=api.getalldata("communes")

#print(all)


