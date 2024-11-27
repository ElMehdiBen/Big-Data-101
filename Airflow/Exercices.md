# Exercise 1: Basic ETL Pipeline
"""
THE ASK:
Create an Airflow DAG that performs the following tasks:
1. Reads a daily temperature data CSV file containing Fahrenheit readings
2. Converts the temperatures from Fahrenheit to Celsius
3. Saves the transformed data to a new CSV file
4. Runs daily and includes basic error handling

STEP BY STEP TUTORIAL:
1. First, set up the imports and default arguments
2. Create the transformation function
3. Define the DAG
4. Create the transformation task
5. Set up the dependencies (single task in this case)
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

# Step 1: Set up default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1)
}

# Step 2: Create transformation function
def transform_temperature(input_path, output_path):
    df = pd.read_csv(input_path)
    df['temperature_celsius'] = (df['temperature_fahrenheit'] - 32) * 5/9
    df.to_csv(output_path, index=False)

# Step 3: Define the DAG
with DAG(
    'temperature_conversion',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Step 4: Create transformation task
    transform_task = PythonOperator(
        task_id='transform_temperature',
        python_callable=transform_temperature,
        op_kwargs={
            'input_path': '/path/to/input.csv',
            'output_path': '/path/to/output.csv'
        }
    )

# Exercise 2: Data Validation Pipeline
"""
THE ASK:
Create a DAG that validates incoming employee data with the following requirements:
1. Check if age and salary values are positive numbers
2. If data is valid, calculate bonus (10% of salary)
3. If data is invalid, log error and send notification
4. Implement branching logic for different data scenarios
5. Ensure the pipeline completes regardless of which path is taken

STEP BY STEP TUTORIAL:
1. Set up imports and create validation function
2. Create processing functions for valid and invalid data
3. Define the DAG with branching logic
4. Create all necessary tasks
5. Set up the correct task dependencies
"""

from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

# Step 1: Create validation function
def validate_data(**context):
    df = pd.read_csv('/path/to/data.csv')
    if (df['age'] > 0).all() and (df['salary'] > 0).all():
        return 'process_valid_data'
    return 'handle_invalid_data'

# Step 2: Create processing functions
def process_valid_data():
    df = pd.read_csv('/path/to/data.csv')
    df['bonus'] = df['salary'] * 0.1
    df.to_csv('/path/to/processed_data.csv', index=False)

def handle_invalid_data():
    print("Invalid data detected")

# Step 3: Define the DAG
with DAG(
    'data_validation_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Step 4: Create tasks
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

    # Step 5: Set up dependencies
    start >> validate >> [process_valid, handle_invalid] >> end

# Exercise 3: Multi-Source Data Integration
"""
THE ASK:
Create a DAG that:
1. Fetches data from both an API and a PostgreSQL database
2. Combines the data from both sources
3. Saves the combined data as a JSON file
4. Handles the dependencies between tasks appropriately
5. Uses XCom to pass data between tasks

STEP BY STEP TUTORIAL:
1. Set up imports and create combination function
2. Define the DAG
3. Create API fetch task
4. Create database fetch task
5. Create data combination task
6. Set up parallel execution of fetch tasks
"""

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
import json

# Step 1: Create combination function
def combine_data(**context):
    api_data = context['task_instance'].xcom_pull(task_ids='fetch_api_data')
    db_data = context['task_instance'].xcom_pull(task_ids='fetch_db_data')
    
    combined_data = {
        'api_metrics': json.loads(api_data),
        'db_metrics': db_data
    }
    
    with open('/path/to/combined_data.json', 'w') as f:
        json.dump(combined_data, f)

# Step 2: Define the DAG
with DAG(
    'multi_source_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Step 3: Create API fetch task
    fetch_api = SimpleHttpOperator(
        task_id='fetch_api_data',
        http_conn_id='api_connection',
        endpoint='/metrics',
        method='GET'
    )
    
    # Step 4: Create database fetch task
    fetch_db = PostgresOperator(
        task_id='fetch_db_data',
        postgres_conn_id='postgres_connection',
        sql="SELECT * FROM metrics WHERE date = '{{ ds }}'"
    )
    
    # Step 5: Create combination task
    combine = PythonOperator(
        task_id='combine_data',
        python_callable=combine_data
    )

    # Step 6: Set up dependencies
    [fetch_api, fetch_db] >> combine

# Exercise 4: Dynamic Task Generation
"""
THE ASK:
Create a DAG that:
1. Processes multiple product categories in parallel
2. Dynamically generates tasks based on a list of categories
3. Ensures all category processing starts after initialization
4. Ensures completion task only runs after all categories are processed
5. Maintains clear task organization despite dynamic generation

STEP BY STEP TUTORIAL:
1. Set up imports and create processing function
2. Create category retrieval function
3. Define the DAG
4. Create start and end tasks
5. Dynamically generate category tasks
6. Set up dependencies
"""

# Step 1: Create processing function
def process_category(category, **context):
    print(f"Processing category: {category}")
    # Add your processing logic here

# Step 2: Create category retrieval function
def get_categories():
    return ['electronics', 'clothing', 'food', 'books']

# Step 3: Define the DAG
with DAG(
    'dynamic_category_processor',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Step 4: Create start and end tasks
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # Step 5: Generate category tasks
    categories = get_categories()
    category_tasks = []

    for category in categories:
        task = PythonOperator(
            task_id=f'process_{category}',
            python_callable=process_category,
            op_kwargs={'category': category}
        )
        category_tasks.append(task)

    # Step 6: Set up dependencies
    start >> category_tasks >> end
