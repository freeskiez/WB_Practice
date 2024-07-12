# ДЗ spark

## 1. Поднимаем все необходимые контейнеры в Docker

![1](./img/1.png)


## 2. Подгружаем данные из Pegas в локальную Kafka

![2](./img/2.png)


## 3. Проверяем. Мы загрузили справочник офисов и их блоков

![3](./img/3.png)

## 4. Создаем пустые таблицы на локальном клике

![4](./img/4.png)

## 5. Будем обогащаться open_date для каждого офиса, предварительно скачиваем csv из Pegas и загружаем в свой локальный клик

![5](./img/5.png)


## 6. Проверяем работоспособность Spark

![6](./img/6.png)


## 7. Читаем данные из Kafka и записываем в клик с обогащением полем open_date

Используем команду:

spark-submit --master spark://spark-master:7077  \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    --executor-cores 1 \
    --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" \
    /opt/spark/Streams/dict_StoragePlace_edu_23/dict_StoragePlace.py

![7](./img/7.png)


## 8. Проверяем работающий процесс Spark

![8](./img/8.png)

## 9. Проверяем итоговую таблицу

![9](./img/9.png)
