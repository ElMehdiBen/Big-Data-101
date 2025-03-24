Chaque projet inclut à la fois les **détails fonctionnels** (le besoin et les attentes) et les **détails des outils** (comment les technologies comme Elasticsearch, Airflow, Kafka, FastAPI, Python Celery, et Debezium peuvent être utilisées). 
Cela offre un cadre clair aux étudiants tout en leur laissant la liberté d’explorer les implémentations. Il n'est pas nécessaire d'utiliser tous les outils proposés, avec un minimum de 3 outils. 

### Conseils pour les étudiants :
- Identifiez les flux de données et les points de traitement pour chaque projet.
- Testez avec des données simulées (ex. logs, capteurs, prix) avant d’explorer des données réelles.
- Utilisez Docker pour déployer les outils (ex. Kafka, Elasticsearch) et simplifier les tests.
- Réfléchissez à la scalabilité et aux scénarios d’échec (ex. surcharge de logs ou panne d’un composant).

Très bonne chance a tous

---

### Projet 1 : Système de suivi en temps réel des logs d'une application
- **Besoin fonctionnel** : Une entreprise fictive souhaite surveiller les logs générés par une application (ex. plateforme e-commerce). Les logs incluent des erreurs, connexions utilisateur ou actions (ex. "Utilisateur X a ajouté un produit au panier"). Le système doit collecter ces logs en temps réel, les centraliser, permettre une recherche rapide (ex. "trouver toutes les erreurs 500 des dernières 24h") et signaler des anomalies critiques (ex. pic d’erreurs).
- **Attentes** :
  - Capture des logs dès leur génération, sans délai notable.
  - Interface (API ou autre) pour consulter les logs ou afficher des statistiques (ex. nombre d’erreurs par heure).
  - Détection et signalement des anomalies (ex. plus de 10 erreurs en 5 minutes).
- **Outils utilisés** :
  - **Debezium** : Capturer les changements dans une base de données (ex. MySQL) utilisée par l’application et les envoyer vers Kafka.
  - **Kafka** : Transférer les logs ou événements en temps réel vers un système de traitement.
  - **FastAPI** : Créer une API pour interagir avec le système (ex. soumettre des logs ou consulter des statistiques).
  - **Elasticsearch** : Stocker et indexer les logs pour une recherche rapide.
  - **Python Celery** : Exécuter des tâches asynchrones comme le traitement des logs (ex. détection d’anomalies) avant leur envoi à Elasticsearch.
- **Contexte** : Simuler une application générant des logs (ex. via une base de données ou des appels API).

---

### Projet 2 : Pipeline ETL pour l'analyse de données de capteurs IoT
- **Besoin fonctionnel** : Une ville intelligente veut analyser les données de capteurs IoT (ex. température, humidité, pollution) dans différents quartiers. Les données arrivent en continu, doivent être nettoyées (ex. supprimer les valeurs aberrantes comme 1000°C), agrégées (ex. moyenne horaire par quartier) et rendues accessibles aux urbanistes via une interface. Le système doit aussi permettre des analyses historiques (ex. évolution de la pollution sur une semaine).
- **Attentes** :
  - Collecte et transformation des données brutes en continu (ex. toutes les 10 minutes).
  - API fournissant des données agrégées (ex. "moyenne de température dans le quartier A") ou brutes.
  - Consultation facile des données historiques (ex. recherche par date ou capteur).
- **Outils utilisés** :
  - **Kafka** : Simuler et transmettre les données des capteurs en streaming.
  - **Airflow** : Orchestrer un pipeline ETL (Extract, Transform, Load) pour nettoyer et agréger les données.
  - **Python Celery** : Effectuer des tâches de transformation (ex. calcul de moyennes ou détection d’anomalies).
  - **Elasticsearch** : Stocker les données transformées pour des analyses futures.
  - **FastAPI** : Fournir une API pour consulter les données agrégées ou brutes.
- **Contexte** : Simuler un flux de données IoT (ex. données aléatoires ou dataset).

---

### Projet 3 : Système de recommandation basé sur les interactions utilisateur
- **Besoin fonctionnel** : Une plateforme de streaming musical veut proposer des recommandations basées sur les interactions des utilisateurs (ex. chansons écoutées, artistes aimés). Lorsqu’un utilisateur agit (ex. écoute une chanson), cette information doit être capturée immédiatement, utilisée pour mettre à jour son profil, et générer des suggestions personnalisées (ex. "Vous pourriez aimer ces chansons"), accessibles via une interface.
- **Attentes** :
  - Suivi des interactions en temps réel (ex. dès un clic sur "play").
  - Mise à jour rapide des recommandations (ex. en moins de 5 secondes).
  - API retournant des suggestions personnalisées (ex. "top 5 chansons pour l’utilisateur X").
- **Outils utilisés** :
  - **Debezium** : Capturer les changements dans une base de données d’interactions (ex. ajout d’un clic).
  - **Kafka** : Diffuser les interactions en temps réel vers un système de traitement.
  - **Python Celery** : Calculer des recommandations (ex. via similarité cosinus) en tâche asynchrone.
  - **Elasticsearch** : Indexer les profils utilisateur et recommandations pour une récupération rapide.
  - **FastAPI** : Exposer une API pour afficher les recommandations personnalisées.
- **Contexte** : Simuler une base d’utilisateurs et leurs interactions (ex. via une base de données ou script).

---

### Projet 4 : Surveillance et alerte sur des flux de données financières
- **Besoin fonctionnel** : Une société de trading souhaite surveiller les prix d’actions ou cryptomonnaies en temps réel, détecter des anomalies (ex. chute de 10 % en 1 minute) et envoyer des alertes (ex. via API ou log). Les données historiques doivent être conservées pour analyse (ex. "quelles anomalies hier ?"), et des rapports périodiques (ex. résumé quotidien) générés.
- **Attentes** :
  - Collecte et analyse des données de prix en continu.
  - Alertes déclenchées immédiatement en cas d’anomalie.
  - Interface pour consulter alertes ou données historiques (ex. "liste des anomalies de la semaine").
  - Rapport quotidien généré automatiquement (ex. nombre d’anomalies par jour).
- **Outils utilisés** :
  - **Kafka** : Recevoir un flux continu de données financières simulées.
  - **Airflow** : Planifier des tâches périodiques pour analyser les tendances sur des fenêtres temporelles.
  - **Python Celery** : Exécuter des tâches asynchrones comme la détection d’anomalies (ex. seuils dépassés).
  - **Elasticsearch** : Stocker les données historiques pour analyse ou visualisation.
  - **FastAPI** : Créer une API pour consulter les alertes ou données brutes.
- **Contexte** : Simuler un flux de données financières (ex. prix aléatoires ou dataset public).

---

### Projet 5 : Journalisation distribuée pour une application multi-services
- **Besoin fonctionnel** : Une startup développe une application avec plusieurs microservices (ex. gestion des utilisateurs, paiements, livraison). Chaque service génère ses logs (ex. "Utilisateur connecté", "Paiement réussi"), et l’équipe veut un système centralisé pour les collecter, analyser et repérer les problèmes (ex. "Pourquoi les paiements échouent-ils souvent ?"), avec des recherches avancées (ex. "tous les logs liés à l’utilisateur X").
- **Attentes** :
  - Centralisation des logs en temps réel ou quasi réel.
  - Recherche rapide (ex. "tous les logs d’erreur du service de paiement aujourd’hui").
  - Tâches périodiques (ex. rapport sur les erreurs chaque matin).
  - API pour interagir avec le système (ex. soumettre un log ou consulter des résultats).
- **Outils utilisés** :
  - **FastAPI** : Simuler plusieurs microservices générant des logs via des endpoints.
  - **Kafka** : Centraliser les logs de chaque service en un flux unique.
  - **Debezium** : Capturer les événements dans une base de données partagée (ex. état des commandes).
  - **Python Celery** : Traiter les logs (ex. filtrer les erreurs critiques) avant stockage.
  - **Elasticsearch** : Indexer les logs pour recherche et visualisation (ex. via Kibana).
  - **Airflow** : Planifier des tâches de maintenance ou d’analyse (ex. rapports quotidiens).
- **Contexte** : Simuler plusieurs services (ex. scripts ou endpoints) générant des logs.
