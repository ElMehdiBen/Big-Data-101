# Exercise 1: Basic ETL Pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1)
}

def transform_temperature(input_path, output_path):
    # Read CSV
    df = pd.read_csv(input_path)
    
    # Convert Fahrenheit to Celsius
    df['temperature_celsius'] = (df['temperature_fahrenheit'] - 32) * 5/9
    
    # Save transformed data
    df.to_csv(output_path, index=False)

with DAG(
    'temperature_conversion',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    transform_task = PythonOperator(
        task_id='transform_temperature',
        python_callable=transform_temperature,
        op_kwargs={
            'input_path': '/path/to/input.csv',
            'output_path': '/path/to/output.csv'
        }
    )

# Exercise 2: Data Validation Pipeline (Beginner-Intermediate)
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
import pandas as pd

def validate_data(**context):
    df = pd.read_csv('/path/to/data.csv')
    
    # Check if data meets criteria
    if (df['age'] > 0).all() and (df['salary'] > 0).all():
        return 'process_valid_data'
    return 'handle_invalid_data'

def process_valid_data():
    df = pd.read_csv('/path/to/data.csv')
    # Process the valid data
    df['bonus'] = df['salary'] * 0.1
    df.to_csv('/path/to/processed_data.csv', index=False)

def handle_invalid_data():
    # Log error and send notification
    print("Invalid data detected")

with DAG(
    'data_validation_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')
    
    validate = BranchPythonOperator(
        task_id='validate_data',
        python_callable=validate_data
    )
    
    process_valid = PythonOperator(
        task_id='process_valid_data',
        python_callable=process_valid_data
    )
    
    handle_invalid = PythonOperator(
        task_id='handle_invalid_data',
        python_callable=handle_invalid_data
    )
    
    end = DummyOperator(
        task_id='end',
        trigger_rule='none_failed_min_one_success'
    )

    start >> validate >> [process_valid, handle_invalid] >> end

# Exercise 3: Multi-Source Data Pipeline (Intermediate)
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
import json

def combine_data(**context):
    # Get data from XCom
    api_data = context['task_instance'].xcom_pull(task_ids='fetch_api_data')
    db_data = context['task_instance'].xcom_pull(task_ids='fetch_db_data')
    
    # Combine and process data
    combined_data = {
        'api_metrics': json.loads(api_data),
        'db_metrics': db_data
    }
    
    # Save combined data
    with open('/path/to/combined_data.json', 'w') as f:
        json.dump(combined_data, f)

with DAG(
    'multi_source_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    fetch_api = SimpleHttpOperator(
        task_id='fetch_api_data',
        http_conn_id='api_connection',
        endpoint='/metrics',
        method='GET'
    )
    
    fetch_db = PostgresOperator(
        task_id='fetch_db_data',
        postgres_conn_id='postgres_connection',
        sql="SELECT * FROM metrics WHERE date = '{{ ds }}'"
    )
    
    combine = PythonOperator(
        task_id='combine_data',
        python_callable=combine_data
    )

    [fetch_api, fetch_db] >> combine

# Exercise 4: Dynamic Task Generation (Intermediate)
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def process_category(category, **context):
    print(f"Processing category: {category}")
    # Add your processing logic here

def get_categories():
    # This could come from a database or API
    return ['electronics', 'clothing', 'food', 'books']

with DAG(
    'dynamic_category_processor',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # Dynamically create tasks for each category
    categories = get_categories()
    category_tasks = []

    for category in categories:
        task = PythonOperator(
            task_id=f'process_{category}',
            python_callable=process_category,
            op_kwargs={'category': category}
        )
        category_tasks.append(task)

    start >> category_tasks >> end
