from kafka import KafkaProducer
import config

producer = KafkaProducer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVER)

def notify(topic, key, value):
    producer.send(topic, key, value)
    

for _ in range(100):
    producer.send('foobar', b'yoo', b'zolo')
    producer.flush()