# Projet-Big-Data
Analyse du commerce extérieur de la France pour l’année 2019

## Authors :
- Youcef CHORFI
- Gontran GILLES

## Dependencies
* Python 2/3 with [NumPy](http://www.numpy.org/)/[SciPy](https://www.scipy.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* Dash
* Plotely 


## Installation

Simply clone the repository:

```bash
git clone https://github.com/Youcef-11/Projet-Big-Data.git
cd Projet-Big-Data
```

## Data viz example


## Description du contenu du dossier
```
- Il faut récupérer les datas depuis https://www.data.gouv.fr/fr/datasets/statistiques-nationales-du-commerce-exterieur/
- Il faut organiser les fichiers comme suit :
- 2 dossiers 'National-2019-export', 'National-2019-import'
	récupérés sur data.gouv
	contient 5 fichiers textes qui sont les données brutes
- Dossier 'Nomenclature' : contient table de passage des codes
	NC8 2019 vers 2020
- Dossier Table_pays : contient le PDF qui nous a permis de créer
	les zones économiques
- Deux fichiers Python :
 	* create_tables.ipynb : prétraitement des données et peuplement des tables
	* dash_gui.py : interface graphique
- 'modélisation_commerce_ex.mcd' : MCD et MLD
- pays_continents.xlsx : récupéré sur internet, a servi à compléter
	la table pays
- 'rapport_projet_big_data_CHORFI_GILLES.pdf'
- 'texte_zone_eco.txt' : nous a servi à créer la table zone-éconimique
```
