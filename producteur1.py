from time import sleep
from random import randint, choice
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
TOPIC = 'test_apache_kafka'
VEHICLE_TYPES = ("car", "truck", "van")

for _ in range(100):
    vehicle_id = randint(10000, 99999)
    vehicle_type = choice(VEHICLE_TYPES)
    message = f"{vehicle_id},{vehicle_type}"
    producer.send(TOPIC, value=message.encode("utf-8"))
    print(f"Produced message: {message}")
    sleep(1)
