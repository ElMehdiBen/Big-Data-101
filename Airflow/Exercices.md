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
