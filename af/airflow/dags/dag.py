import psycopg2
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime as dt
from clickhouse_driver import Client


default_args = {
    'owner': 'kotov',
    'start_date': dt(2024, 8, 4)
}

dag = DAG(
    dag_id='test_dag',
    default_args=default_args,
    schedule_interval='1 * * * *',
    description='test dag',
    catchup=False,
    max_active_runs=1
)


def ch_engine():
    try:
        print('Попытка коннекта к CH')
        with open('/opt/airflow/dags/credentials.json') as json_file:
            data = json.load(json_file)
        client = Client(
            data['clickhouse'][0]['host'],
            user=data['clickhouse'][0]['user'],
            password=data['clickhouse'][0]['password'],
            port=data['clickhouse'][0]['port'],
            verify=False,
            settings={"numpy_columns": True, 'use_numpy': True},
            compression=False
        )
        return client
    except Exception as e:
        print(f"Ошибка при попытке коннекта к ClickHouse: {e}")
        return None


def pg_engine():
    try:
        print('Попытка коннекта к PG')
        with open('/opt/airflow/dags/credentials.json') as json_file:
            data = json.load(json_file)
        client = psycopg2.connect(
            host=data['postgres'][0]['host'],
            user=data['postgres'][0]['user'],
            password=data['postgres'][0]['password'],
            port=data['postgres'][0]['port'],
            dbname=data['postgres'][0]['dbname']
        )
        return client
    except Exception as e:
        print(f"Ошибка при попытке коннекта к PostgreSQL: {e}")
        return None


#  моделируем агрегацию данных внутри клика с последующим заполнением витрины в схеме report
def main():
    q = f'''
        INSERT INTO report.kotov_t1
        select count(shk_id) qty
            , lostreason_id
            , state_id_last
        from default.kotov_t1
        group by lostreason_id, state_id_last
    '''
    client_ch = ch_engine()
    client_ch.execute(q)


#  импортируем данные из клика (report) в пг
def import_pg():
    client_ch = ch_engine()
    client_pg = pg_engine()
    cursor = client_pg.cursor()

    q = f'''
        select now() dt_last_load
            , qty
            , lostreason_id
            , state_id_last
        from report.kotov_t1 final
    '''
    df = client_ch.query_dataframe(q)
    df = df.to_json(orient="records", date_format="iso", date_unit="s")
    cursor.execute(f"CALL sync.kotov_t2_importfromclick(_src := '{df}')")
    client_pg.commit()
    cursor.close()
    client_pg.close()


task_1 = PythonOperator(
    task_id='task_1',
    python_callable=main,
    dag=dag
)


task_2 = PythonOperator(
    task_id='task_2',
    python_callable=import_pg,
    dag=dag
)


task_1 >> task_2
