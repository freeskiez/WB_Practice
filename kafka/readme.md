# Работа с kafka

## 1. Билд контейнера с kafka

![1](./img/1.png)
[docker-compose-kafka-sasl.yml](./docker-compose-kafka-sasl.yml)

[client.properties](./client.properties)

[kafka_server_jaas.conf](./kafka_server_jaas.conf)

[zookeeper_jaas.conf](./zookeeper_jaas.conf)

## 2. Заливка данных из клика в топик кафки

![2](./img/2.png)
[producer_with_sasl.py](./producer_with_sasl.py)

## 3. Проверка залитых данных
![3](./img/3.png)

## 4. Чтение данных с кафки

![4](./img/4.png)
[consumer_with_SASL.py](./consumer_with_SASL.py)
