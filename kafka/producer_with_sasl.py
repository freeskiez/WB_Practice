from confluent_kafka import Producer
from clickhouse_driver import Client
import json
import time

config = {
    'bootstrap.servers': 'localhost:9093',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

producer = Producer(**config)


def connect_CH():
    with open(f"/Users/freeskiez/PycharmProjects/WB_Practice/kafka/secrets/ch_db.json") as json_file:
        param_connect = json.load(json_file)
        for _ in range(7):
            try:
                client = Client(param_connect['server'][0]['host'],
                                user=param_connect['server'][0]['user'],
                                password=param_connect['server'][0]['password'],
                                port=param_connect['server'][0]['port'],
                                verify=False,
                                database='',
                                settings={"numpy_columns": True, 'use_numpy': True},
                                compression=True)
                return client
            except Exception as e:
                print(e, "Нет коннекта к КликХаус")
                time.sleep(60)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def send_message(data):
    try:
        message = json.dumps(data)
        producer.produce('click_topic', value=message.encode('utf-8'), callback=delivery_report)
        producer.poll(0)
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")


def main():
    client = connect_CH()
    result = client.execute("""
        select shk_id, tare_id
        from tmp.kotov_t1
        limit 10
    """)
    for row in result:
        data = {'shk_id': int(row[0]), 'tare_id': int(row[1])}
        send_message(data)
        producer.flush()


if __name__ == '__main__':
    main()