from decouple import config

KAFKA_BOOTSTRAP_SERVER=config('KAFKA_BOOTSTRAP_SERVER')
GOLD_PRICE_TOPIC=config('GOLD_PRICE_TOPIC', default='goldprice')