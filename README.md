# Guide de mise en place d'un pipeline ETL en streaming avec Kafka et MySQL

Ce guide détaille toutes les étapes nécessaires pour configurer un pipeline de données en streaming permettant de décharger les autoroutes nationales grâce à l'analyse des données de trafic routier provenant de différents péages.

## Objectifs

Créer un pipeline de données en streaming pour collecter les données des véhicules depuis Kafka et les stocker dans une base de données MySQL.

## Prérequis
- Docker et Docker Compose installés.
- Python 3 installé avec pip.

---

## Étapes d'exécution

### Étape 1 : Télécharger et extraire Kafka
1. Téléchargez Kafka :
   ```bash
   wget https://archive.apache.org/dist/kafka/3.7.0/kafka_2.12-3.7.0.tgz
   ```
2. Extrayez Kafka :
   ```bash
   tar -xzf kafka_2.12-3.7.0.tgz
   ```
   Une fois extrait, un répertoire nommé `kafka_2.12-3.7.0` sera créé.

---

### Étape 2 : Configurer KRaft et démarrer le serveur Kafka
1. Accédez au répertoire Kafka :
   ```bash
   cd kafka_2.12-3.7.0
   ```
2. Générez un identifiant unique pour le cluster Kafka :
   ```bash
   KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
   ```
3. Configurez les répertoires de logs avec l'identifiant généré :
   ```bash
   bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
   ```
4. Démarrez le serveur Kafka :
   ```bash
   bin/kafka-server-start.sh config/kraft/server.properties
   ```
   Vérifiez les messages indiquant que le serveur a démarré avec succès.

---

### Étape 3 : Configurer le serveur MySQL et créer la base de données
1. Lancez le serveur MySQL via l'IDE ou votre interface préférée.
2. Connectez-vous au serveur MySQL :
   ```bash
   mysql --host=mysql --port=3306 --user=root --password=<votre_mot_de_passe>
   ```
3. Créez une base de données `tolldata` :
   ```sql
   CREATE DATABASE tolldata;
   ```
4. Créez une table `livetolldata` pour stocker les données de trafic :
   ```sql
   USE tolldata;
   CREATE TABLE livetolldata (
       timestamp DATETIME,
       vehicle_id INT,
       vehicle_type CHAR(15),
       toll_plaza_id SMALLINT
   );
   ```
5. Quittez MySQL :
   ```bash
   exit
   ```

---

### Étape 4 : Installer les modules Python nécessaires
1. Installez le module Kafka pour Python :
   ```bash
   pip3 install kafka-python
   ```
2. Installez le module MySQL pour Python :
   ```bash
   pip3 install mysql-connector-python==8.0.31
   ```

---

### Étape 5 : Créer le pipeline de données pour les données de trafic
#### 1. Créer un sujet Kafka
- Créez un sujet Kafka nommé `toll` :
  ```bash
  bin/kafka-topics.sh --create --topic toll --bootstrap-server localhost:9092
  ```

#### 2. Configurer le générateur de données
1. Téléchargez le fichier `toll_traffic_generator.py` :
   ```bash
   wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/toll_traffic_generator.py
   ```
2. Ouvrez le fichier et configurez le sujet à `toll`.
3. Lancez le générateur :
   ```bash
   python3 toll_traffic_generator.py
   ```

#### 3. Configurer le lecteur de données en streaming
1. Téléchargez le fichier `streaming-data-reader.py` :
   ```bash
   wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/vVxmU5uatDowvAIKRZrFjg/streaming-data-reader.py
   ```
2. Modifiez les paramètres suivants dans le fichier :
   - **TOPIC** : `toll`
   - **DATABASE** : `tolldata`
   - **USERNAME** : `root`
   - **PASSWORD** : `<votre_mot_de_passe>`
3. Lancez le lecteur de données :
   ```bash
   python3 streaming-data-reader.py
   ```

#### 4. Vérifier les données dans MySQL
1. Connectez-vous à MySQL :
   ```bash
   mysql --host=mysql --port=3306 --user=root --password=<votre_mot_de_passe>
   ```
2. Affichez les 10 premières lignes de la table :
   ```sql
   SELECT * FROM livetolldata LIMIT 10;
   ```

---

## Résultat attendu
À la fin de ce processus, vous devriez voir les données en streaming insérées en temps réel dans la table `livetolldata` de la base de données MySQL.

---


