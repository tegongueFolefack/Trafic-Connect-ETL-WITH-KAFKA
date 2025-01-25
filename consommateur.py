from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
import mysql.connector

def consume_messages():
    consumer = KafkaConsumer('test_apache_kafka', bootstrap_servers='localhost:9092')
    connection = mysql.connector.connect(
        host='localhost',
        database='toll_data',
        user='root',
        password='medarine672'
    )
    cursor = connection.cursor()

    for msg in consumer:
        message = msg.value.decode("utf-8")
        vehicle_id, vehicle_type = message.split(",")
        sql = "INSERT INTO vehicles (vehicle_id, vehicle_type) VALUES (%s, %s)"
        cursor.execute(sql, (vehicle_id, vehicle_type))
        connection.commit()
        print(f"Inserted {vehicle_id} of type {vehicle_type} into database")

    cursor.close()
    connection.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

dag = DAG('toll_data_pipeline', default_args=default_args, schedule_interval='@once')

consume_task = PythonOperator(
    task_id='consume_toll_data',
    python_callable=consume_messages,
    dag=dag
)
