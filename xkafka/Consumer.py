from kafka import KafkaConsumer
import config
consumer = KafkaConsumer(bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVER)
consumer.subscribe(['pnj'])
while True:
    msg = next(consumer)
    print('topoic {} key {} value {}'.format(msg.topic, msg.key, msg.value))
    pass