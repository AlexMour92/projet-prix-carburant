Ce projet est une application d'analyse de données journalières qui suit et analyse les prix des carburants dans la région Île-de-France. L'objectif est de créer une chaine décisionnelle complète:
  * Création d'un **pipeline ETL** en **Python** pour récupérer les données de l'API du gouvernement [Prix des carburants - Flux instantanées - v2](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/).
  * Mise en place d'un **entrepôt de données** sur **Google BigQuery**.
  * Exploitation et visualisation des données récoltées via un [**dashboard**](https://lookerstudio.google.com/s/gkexJF_uqkI) sur **Google Looker Studio**. Le dashboard est centré sur les **décisions d'achats**:
    - Décisions d'achats de voiture grâce à l'évolution des prix et les taux de détention des carburants.
    - Décisions d'achats de carburants grâce aux prix journaliers.
    - Choix de la stations la plus avantageuse autour de moi grace aux données géographiques.
  * Réalisation de prédictions sur les séries temporelles.

# Pipeline ETL et entrepôt de données

L'application récupère automatiquement les données de l'API gouvernementale, les traite, et les stocke dans une base de données cloud pour une analyse ultérieure.

## Stack Technique

### Backend

  * **Python 3.12**: Langage principal pour le développement backend.
  * **Google Cloud BigQuery**: Base de données cloud pour le stockage et l'analyse des données à grande échelle.

### Infrastructure Cloud et CI/CD

  * **Google Cloud Platform (GCP)**: Plateforme cloud pour l'hébergement et le déploiement de l'application.
  * **Cloud Run**: Service serverless pour l'exécution de conteneurs.
  * **GitHub Actions**: Utilisé pour l'intégration continue et le déploiement continu (CI/CD).
  * **Docker**: Conteneurisation de l'application pour un déploiement cohérent et portable.

### Tests

  * **Unittest**: Framework de test unitaire Python pour assurer la qualité et la fiabilité du code.

### Gestion des données

  * **API Gouvernementale**: Source des données sur les prix des carburants.
  * **ETL (Extract, Transform, Load)**: Processus automatisé pour extraire, transformer et charger les données.

## Architecture du Projet

L'application suit une architecture modulaire :
### Module d'Extraction des Données:
  * Utilise requests pour récupérer les données de l'API gouvernementale.
  * Convertit les données brutes en DataFrame pandas.
### Module de Traitement des Données:
Nettoie et transforme les données avec pandas.
Prépare les données pour le stockage dans BigQuery.
### Module de Stockage des Données:
  * Utilise la bibliothèque Google Cloud pour interagir avec BigQuery.
### Pipeline ETL:
  * Orchestré par Cloud Run, s'exécute à intervalles réguliers.
  * Assure l'intégrité et la cohérence des données à chaque mise à jour.
### Tests Automatisés:
  * Suite de tests unitaires complète pour chaque module.
  * Intégration des tests dans le pipeline CI/CD.

## Déploiement et CI/CD

Utilisation de GitHub Actions pour automatiser les tests, la construction de l'image Docker, et le déploiement sur Cloud Run.
Processus de déploiement en deux étapes : test sur un environnement de staging avant le déploiement en production.
Gestion sécurisée des secrets et des variables d'environnement via GitHub Secrets et Cloud Run.

## Points Forts du Projet

  * **Scalabilité**: Conçu pour gérer de grands volumes de données grâce à l'utilisation de BigQuery et Cloud Run.
  * **Automatisation**: Pipeline ETL entièrement automatisé, de la collecte des données au stockage.
  * **Sécurité**: Gestion sécurisée des credentials et des données sensibles.
  * **Maintenabilité**: Architecture modulaire et tests exhaustifs pour faciliter la maintenance et les évolutions futures.
  * **Analyse journalière**: Capacité à fournir des insights actualisés sur les tendances des prix des carburants.

# Dashboard et Visualisation des Données

Pour exploiter les données récoltées par notre pipeline ETL, j'ai créé un dashboard interactif sur Google Looker Studio. Ce dashboard offre une vue d'ensemble complète et détaillée des prix des carburants en Île-de-France, permettant aux utilisateurs d'analyser les tendances et de prendre des **décisions d'achats éclairées**.

## Caractéristiques principales du dashboard :

### Vue d'ensemble des prix moyens :

  * **Affichage en temps réel des prix moyens journaliers** pour chaque type de carburant (Gazole, GPLc, Sans Plomb 95, Sans Plomb 98, E10, E85).
  * Indication des **variations de prix** par rapport à la période précédente.

### Évolution des prix :

  * Graphique linéaire montrant l'**évolution des prix journaliers moyens** pour tous les types de carburants.
  * Permet de visualiser les tendances sur une période donnée.

### Taux de détention en Île-de-France :

  * Graphique en barres illustrant la **disponibilité de chaque type de carburant** dans les stations-service de la région.

### Stations les moins chères :

  * Tableau listant les stations-service proposant les **prix les plus bas**, avec des filtres pour le type de carburant, le département et la ville.

### Ma station :

  * Section personnalisable permettant aux utilisateurs de suivre les prix d'une station spécifique.
  * Affichage des prix actuels et de leur évolution dans le temps.
  * Carte interactive montrant l'emplacement de la station sélectionnée.


### Carte des prix :

  * Carte interactive de l'Île-de-France affichant les stations-service avec un code couleur basé sur leurs prix.
  * Filtres pour sélectionner le type de carburant et le département.

## Avantages du dashboard :

  * **Visibilité en temps réel** : Les utilisateurs peuvent accéder aux dernières données sur les prix des carburants, mises à jour quotidiennement.
  * **Analyse comparative** : Facilite la comparaison des prix entre différents types de carburants et différentes zones géographiques.
  * **Personnalisation** : Les utilisateurs peuvent se concentrer sur les données les plus pertinentes pour eux, que ce soit un type de carburant spécifique ou une zone géographique particulière.
  * **Aide à la décision** : Fournit des informations précieuses pour les consommateurs cherchant à optimiser leurs dépenses en carburant, ainsi que pour les analystes du marché.

Ce dashboard représente la finalité de notre chaîne décisionnelle, transformant les données brutes collectées en informations exploitables et visuellement attrayantes. Il démontre la puissance de l'analyse de données appliquée à un cas d'usage concret et quotidien.

# Modèle Prédictif avec XGBoost

Dans le cadre de l'extension de notre projet d'analyse des prix des carburants, nous avons développé un modèle prédictif utilisant XGBoost. Cette étape préparatoire vise à établir une méthodologie robuste pour la prédiction des prix des carburants, en attendant d'avoir suffisamment de données pour l'Île-de-France.

## Étude de Cas : Prédiction des Prix du Gazole A1 aux USA
 * **Objectif:**
   Développer et tester un modèle prédictif pour les prix des carburants, applicable à terme aux données d'Île-de-France.
 * **Données:**
   Utilisation des données historiques des prix du carburant A1 aux États-Unis (All Grades All Formulations Retail Gasoline Prices) de 1995 à 2021.
   
## Méthodologie

### Analyse Exploratoire des Données :
L'analyse a révélé trois caractéristiques clés des données :

 * Une faible saisonnalité
 * Une forte influence des valeurs récentes de la série
 * Un caractère non-stationnaire de la série

### Feature Engineering :
Basé sur les résultats de l'analyse exploratoire, j'ai créé plusieurs features pour améliorer les performances du modèle.

### Modélisation avec XGBoost :

 * Entraînement du modèle XGBoost pour des prédictions sur 6 mois (1 prédiction par semaine).
 * Optimisation des hyperparamètres par Grid Search avec Cross Validation pour améliorer la précision.


### Évaluation du Modèle :
Le modèle XGBoost est comparé à un modèle de régression linéaire simple :

 * **XGBoost RMSE** : 0.05 dollars/gallon sur les données de test
 * **Modèle linéaire RMSE** : 0.88 dollars/gallon sur les données de test

Le modèle XGBoost montre une amélioration significative, avec une erreur 17.6 fois plus faible que le modèle linéaire.

![image](https://github.com/user-attachments/assets/743a8bc4-e0ed-42dc-98d4-303b929e0739)


## Résultats et Interprétation

L'erreur de 0.05 dollars/gallon du modèle XGBoost représente environ 1.9% d'un prix moyen typique de 2.7 dollars/gallon.
En comparaison, l'erreur du modèle linéaire (0.88 dollars/gallon) représenterait environ 33% du même prix moyen.
Cette précision accrue démontre la capacité de XGBoost à capturer les relations non linéaires complexes dans les données de prix des carburants.

## Intégration Future au Dashboard
À terme, les prédictions générées par ce modèle seront intégrées à notre dashboard Looker Studio, offrant aux utilisateurs :

 * Des prévisions à court terme des prix des carburants en Île-de-France.
 * Des recommandations pour optimiser les décisions d'achat de carburant.
 * Une vue prospective pour aider à la planification budgétaire des consommateurs et des entreprises.

Cette approche prédictive complète la chaîne décisionnelle, en ajoutant une dimension prospective à l'analyse des prix des carburants.
