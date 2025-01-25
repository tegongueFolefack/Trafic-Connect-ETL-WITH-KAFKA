"""
Top Traffic Simulator
"""

from time import sleep, time, ctime  # Importation des fonctions pour gérer les pauses et les horodatages
from random import random, randint, choice  # Importation de fonctions pour générer des valeurs aléatoires
from kafka import KafkaProducer  # Importation de KafkaProducer pour produire des messages Kafka

# Création du producteur Kafka et connexion au serveur Kafka local
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Définition du sujet Kafka où les messages seront envoyés
TOPIC = 'toll'

# Liste des types de véhicules simulés pour le péage, avec une proportion plus élevée de "car" (voiture)
VEHICLE_TYPES = ("car", "car", "car", "car", "car", "car", "car", "car",
                 "car", "car", "car", "truck", "truck", "truck",
                 "truck", "van", "van")

# Boucle pour générer et envoyer un nombre défini de messages au sujet Kafka
for _ in range(100000):
    vehicle_id = randint(10000, 10000000)  # Génère un identifiant unique aléatoire pour chaque véhicule
    vehicle_type = choice(VEHICLE_TYPES)  # Sélectionne un type de véhicule de manière aléatoire dans VEHICLE_TYPES
    now = ctime(time())  # Génère un horodatage actuel sous format lisible (par ex. 'Tue Oct 29 19:19:11 2024')
    plaza_id = randint(4000, 4010)  # Génère un ID de péage aléatoire dans une plage spécifiée

    # Création d'un message au format "horodatage, identifiant véhicule, type de véhicule, ID de péage"
    message = f"{now},{vehicle_id},{vehicle_type},{plaza_id}"
    message = bytearray(message.encode("utf-8"))  # Conversion du message en bytearray pour Kafka

    # Affichage dans la console pour suivi visuel de chaque véhicule traité
    print(f"A {vehicle_type} has passed by the toll plaza {plaza_id} at {now}.")

    # Envoi du message au sujet Kafka spécifié
    producer.send(TOPIC, message)

    # Pause aléatoire entre les messages pour simuler le passage des véhicules en temps réel
    sleep(random() * 2)


