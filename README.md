Ce projet est une application d'analyse de données journalières qui suit et analyse les prix des carburants dans la région Île-de-France. L'objectif est de créer une chaine décisionnelle complète:
  * Création d'un **pipeline ETL** en **Python** pour récupérer les données de l'API du gouvernement [Prix des carburants - Flux instantanées - v2](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/).
  * Mise en place d'un **entrepôt de données** sur **Google BigQuery**.
  * Exploitation et visualisation des données récoltées via un [**dashboard** sur **Google Looker Studio**.](https://lookerstudio.google.com/s/gkexJF_uqkI)
  * Réalisation de prédiction sur les séries temporelles.

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

Pour exploiter les données récoltées par notre pipeline ETL, j'ai créé un dashboard interactif sur Google Looker Studio. Ce dashboard offre une vue d'ensemble complète et détaillée des prix des carburants en Île-de-France, permettant aux utilisateurs d'analyser les tendances et de prendre des décisions éclairées.

## Caractéristiques principales du dashboard :

### Vue d'ensemble des prix moyens :

  * Affichage en temps réel des prix moyens pour chaque type de carburant (Gazole, GPLc, Sans Plomb 95, Sans Plomb 98, E10, E85).
  * Indication des variations de prix par rapport à la période précédente.

### Évolution des prix :

  * Graphique linéaire montrant l'évolution des prix journaliers moyens pour tous les types de carburants.
  * Permet de visualiser les tendances sur une période donnée.

### Taux de détention en Île-de-France :

  * Graphique en barres illustrant la disponibilité de chaque type de carburant dans les stations-service de la région.

### Stations les moins chères :

  * Tableau listant les stations-service proposant les prix les plus bas, avec des filtres pour le type de carburant, le département et la ville.

## Ma station :

  * Section personnalisable permettant aux utilisateurs de suivre les prix d'une station spécifique.
  * Affichage des prix actuels et de leur évolution dans le temps.
  * Carte interactive montrant l'emplacement de la station sélectionnée.


## Carte des prix :

  * Carte interactive de l'Île-de-France affichant les stations-service avec un code couleur basé sur leurs prix.
  * Filtres pour sélectionner le type de carburant et le département.

## Avantages du dashboard :

  * Visibilité en temps réel : Les utilisateurs peuvent accéder aux dernières données sur les prix des carburants, mises à jour quotidiennement.
  * Analyse comparative : Facilite la comparaison des prix entre différents types de carburants et différentes zones géographiques.
  * Personnalisation : Les utilisateurs peuvent se concentrer sur les données les plus pertinentes pour eux, que ce soit un type de carburant spécifique ou une zone géographique particulière.
  * Aide à la décision : Fournit des informations précieuses pour les consommateurs cherchant à optimiser leurs dépenses en carburant, ainsi que pour les analystes du marché.

Ce dashboard représente la finalité de notre chaîne décisionnelle, transformant les données brutes collectées en informations exploitables et visuellement attrayantes. Il démontre la puissance de l'analyse de données appliquée à un cas d'usage concret et quotidien.
