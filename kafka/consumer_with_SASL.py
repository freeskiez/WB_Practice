from confluent_kafka import Consumer, KafkaError

config = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

consumer = Consumer(config)
consumer.subscribe(['click_topic'])

def main():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
            # Проверка, что сообщение не пустое
            if msg.value() is not None:
                print(f"Received message: {msg.value().decode('utf-8')}")
            else:
                print("Received an empty message")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
