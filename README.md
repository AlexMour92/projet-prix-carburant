# projet-prix-carburant

Ce projet est une application d'analyse de données journalières qui suit et analyse les prix des carburants dans la région Île-de-France. L'objectif est de créer une chaine décisionnelle complète:
  * Création d'un **pipeline ETL** en **Python** pour récupérer les données de l'API du gouvernement [Prix des carburants - Flux instantanées - v2](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/api/).
  * Mise en place d'un **entrepôt de données** sur **Google BigQuery**.
  * Exploitation et visualisation des données récoltées via un **dashboard** sur **Google Looker Studio**.
  * Réalisation de prédiction sur les séries temporelles.

## Pipeline ETL

L'application récupère automatiquement les données de l'API gouvernementale, les traite, et les stocke dans une base de données cloud pour une analyse ultérieure.

### Stack Technique

#### Backend

  * **Python 3.12**: Langage principal pour le développement backend.
  * **Google Cloud BigQuery**: Base de données cloud pour le stockage et l'analyse des données à grande échelle.

#### Infrastructure Cloud et CI/CD

  * **Google Cloud Platform (GCP)**: Plateforme cloud pour l'hébergement et le déploiement de l'application.
  * **Cloud Run**: Service serverless pour l'exécution de conteneurs.
  * **GitHub Actions**: Utilisé pour l'intégration continue et le déploiement continu (CI/CD).
  * **Docker**: Conteneurisation de l'application pour un déploiement cohérent et portable.

#### Tests

  * **Unittest**: Framework de test unitaire Python pour assurer la qualité et la fiabilité du code.

#### Gestion des données

  * **API Gouvernementale**: Source des données sur les prix des carburants.
  * **ETL (Extract, Transform, Load)**: Processus automatisé pour extraire, transformer et charger les données.

