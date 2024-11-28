from airflow import DAG

from airflow.operators.python import PythonOperator

from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

import json

import requests

import csv

import psycopg2

from io import StringIO


# WebHDFS configuration

WEBHDFS_HOST = "http://20.119.81.84:9870"

WEBHDFS_USER = "hdfs"

HDFS_PATH = "/csvs"


default_args = {

    'owner': 'airflow',

    'depends_on_last_run': False,

    'email_on_failure': False,

    'email_on_retry': False,

    'retries': 1,

    'retry_delay': timedelta(minutes=5),

}


# PostgreSQL configuration

PG_HOST = '20.119.81.84'

PG_DATABASE = 'postgres'

PG_USER = 'postgres'

PG_PASSWORD = 'mysecretpassword'

PG_QUERY = 'SELECT * FROM companies'


def fetch_from_postgresql(**context):

    """Fetch data from PostgreSQL database and store as CSV in XCom"""

    # Connect to PostgreSQL

    conn = psycopg2.connect(

        host=PG_HOST,

        database=PG_DATABASE,

        user=PG_USER,

        password=PG_PASSWORD

    )

    cursor = conn.cursor()

    cursor.execute(PG_QUERY)

    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    

    # Write data to CSV format

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(column_names)  # Write header

    writer.writerows(rows)

    output.seek(0)

    

    # Push CSV data to XCom

    context['task_instance'].xcom_push(key='csv_data', value=output.getvalue())

    

    cursor.close()

    conn.close()


def send_to_webhdfs(**context):

    """Send the CSV data to WebHDFS"""

    csv_data = context['task_instance'].xcom_pull(key='csv_data', task_ids='fetch_data_from_postgresql')

    

    # WebHDFS REST API endpoint for creating a file

    webhdfs_url = f"{WEBHDFS_HOST}/webhdfs/v1"

    

    # Create a unique filename for the CSV

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"{HDFS_PATH}/data_{timestamp}.csv"

    

    # WebHDFS CREATE operation

    create_url = f"{webhdfs_url}{filename}?op=CREATE&user.name={WEBHDFS_USER}&overwrite=true"

    

    # First request to get the redirect URL

    init_response = requests.put(create_url, allow_redirects=False)

    if init_response.status_code != 307:

        raise Exception(f"Failed to initialize WebHDFS upload: {init_response.text}")

    

    # Get the redirect URL for actual data upload

    redirect_url = init_response.headers['Location']

    if "deb88c0077a4" in redirect_url:

        redirect_url = redirect_url.replace("9864", "9862").replace("deb88c0077a4", "20.119.81.84")

    if "2af3514e8965" in redirect_url:

        redirect_url = redirect_url.replace("9864", "9861").replace("2af3514e8965", "20.119.81.84")

    

    # Send the actual data

    upload_response = requests.put(

        redirect_url,

        data=csv_data,

        headers={'Content-Type': 'text/csv'}

    )

    

    if upload_response.status_code != 201:

        raise Exception(f"Failed to upload file to HDFS: {upload_response.text}")


with DAG(

    'postgresql_to_webhdfs_pipeline',

    default_args=default_args,

    description='Fetch data from PostgreSQL and send to WebHDFS',

    schedule_interval=timedelta(days=1),

    start_date=days_ago(1),

    catchup=False,

    tags=['postgresql', 'webhdfs'],

) as dag:


    # Task to fetch data from PostgreSQL

    fetch_data_from_postgresql = PythonOperator(

        task_id='fetch_data_from_postgresql',

        python_callable=fetch_from_postgresql,

        provide_context=True,

    )


    # Task to send data to WebHDFS

    send_to_hdfs = PythonOperator(

        task_id='send_to_hdfs',

        python_callable=send_to_webhdfs,

        provide_context=True,

    )


    # Set task dependencies

    fetch_data_from_postgresql >> send_to_hdfs
