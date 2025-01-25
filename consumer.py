from kafka import KafkaConsumer
import json

# Crée un consommateur Kafka qui désérialise les messages au format JSON
consumer = KafkaConsumer(
    'bankbranch',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Boucle pour lire les messages depuis le sujet et les afficher
for message in consumer:
    print(f"Received message: {message.value}")
