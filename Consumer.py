from kafka import KafkaConsumer
import config
consumer = KafkaConsumer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVER)
consumer.subscribe(['pnj'])
for mgs in consumer:
    print(mgs)