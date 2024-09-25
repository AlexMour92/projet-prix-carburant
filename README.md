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
