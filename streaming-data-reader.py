"""
Streaming data consumer
"""
from datetime import datetime  # Importation du module pour manipuler les dates et heures
from kafka import KafkaConsumer  # Importation de KafkaConsumer pour consommer des messages Kafka
import mysql.connector  # Importation du module MySQL pour la connexion à la base de données

# Configuration des paramètres de connexion
TOPIC = 'toll'  # Nom du sujet Kafka à partir duquel consommer les messages
DATABASE = 'tolldata'  # Nom de la base de données MySQL cible
USERNAME = 'root'  # Nom d'utilisateur de la base de données MySQL
PASSWORD = 'medarine672'  # Mot de passe de l'utilisateur MySQL

print("Connecting to the database")
try:
    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(host='localhost', database=DATABASE, user=USERNAME, password=PASSWORD)
except Exception:
    # Si la connexion échoue, afficher un message d'erreur
    print("Could not connect to database. Please check credentials")
else:
    # Si la connexion réussit, afficher un message de confirmation
    print("Connected to database")
    
# Création d'un curseur pour exécuter les requêtes SQL
cursor = connection.cursor()

print("Connecting to Kafka")
# Connexion au sujet Kafka en créant un consommateur pour le sujet spécifié
consumer = KafkaConsumer(TOPIC)
print("Connected to Kafka")
print(f"Reading messages from the topic {TOPIC}")

# Boucle pour consommer et traiter chaque message dans le sujet Kafka
for msg in consumer:

    # Extraction du message Kafka reçu
    message = msg.value.decode("utf-8")  # Décodage du message en format texte UTF-8

    # Transformation du message pour adapter le format de date au schéma de la base de données
    (timestamp, vehcile_id, vehicle_type, plaza_id) = message.split(",")  # Séparation des éléments du message

    # Conversion du timestamp en format standard SQL 'YYYY-MM-DD HH:MM:SS'
    dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

    # Insertion des données dans la table 'livetolldata' de la base de données
    sql = "insert into livetolldata values(%s,%s,%s,%s)"
    result = cursor.execute(sql, (timestamp, vehcile_id, vehicle_type, plaza_id))
    
    # Confirmation visuelle de l'insertion de chaque véhicule dans la base de données
    print(f"A {vehicle_type} was inserted into the database")
    connection.commit()  # Validation de la transaction

# Fermeture de la connexion une fois tous les messages traités
connection.close()

