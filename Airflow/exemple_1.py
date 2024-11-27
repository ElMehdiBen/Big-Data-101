from airflow import DAG
from airflow.operators.python_operator import PythonOperator

dag = DAG('exemple_1')

def extract_data():
    # Extract data from the database
    pass

def load_data():
    # Load data into the data warehouse
    pass

extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

extract_data_task >> load_data_task
