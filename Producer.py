from kafka import KafkaProducer
import config

producer = KafkaProducer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVER)

def notify(topic, key, value):
    producer.send(topic, value, key)
    