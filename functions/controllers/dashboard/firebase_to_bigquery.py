from google.cloud import firestore
from google.cloud import bigquery
import time

# Replace with your project ID and collection name
project_id = "simplitracapp"
collection_name = "test2"

# Replace with your BigQuery dataset and table names
dataset_id = "firestore_export"
table_id = "bi_viz"

# Firestore client
firestore_client = firestore.Client(project=project_id)
collection_ref = firestore_client.collection(collection_name)

# BigQuery client
bigquery_client = bigquery.Client(project=project_id)

def check_and_create_table():
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    try:
        bigquery_client.get_table(table_ref)
        print(f"Table {table_id} already exists.")
    except:
        schema = [
            bigquery.SchemaField("admin", "BOOL", mode="NULLABLE"),
            bigquery.SchemaField("coordinates", "GEOGRAPHY", mode="NULLABLE"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("email", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("f_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("google_id", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("l_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("last_login", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("picture", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
        ]
        
        table = bigquery.Table(table_ref, schema=schema)
        bigquery_client.create_table(table)
        print(f"Created table {table_id}.")

def update_or_insert_user(doc_data):
    user_id = doc_data["user_id"]
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    
    query = f"""
    SELECT user_id FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE user_id = '{user_id}'
    """
    
    query_job = bigquery_client.query(query)
    results = query_job.result()
    
    if results.total_rows > 0:
        # Update user data
        update_query = f"""
        UPDATE `{project_id}.{dataset_id}.{table_id}`
        SET admin = @admin,
            coordinates = @coordinates,
            created_at = @created_at,
            email = @Email,
            f_name = @f_name,
            google_id = @google_id,
            l_name = @l_name,
            last_login = @last_login,
            picture = @picture
        WHERE user_id = @user_id
        """
        
        query_params = [
            bigquery.ScalarQueryParameter("admin", "BOOL", doc_data.get("admin")),
            bigquery.ScalarQueryParameter("coordinates", "GEOGRAPHY", doc_data.get("coordinates")),
            bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", doc_data.get("created_at")),
            bigquery.ScalarQueryParameter("email", "STRING", doc_data.get("email")),
            bigquery.ScalarQueryParameter("f_name", "STRING", doc_data.get("f_name")),
            bigquery.ScalarQueryParameter("google_id", "STRING", doc_data.get("google_id")),
            bigquery.ScalarQueryParameter("l_name", "STRING", doc_data.get("l_name")),
            bigquery.ScalarQueryParameter("last_login", "TIMESTAMP", doc_data.get("last_login")),
            bigquery.ScalarQueryParameter("picture", "STRING", doc_data.get("picture")),
            bigquery.ScalarQueryParameter("user_id", "STRING", doc_data.get("user_id")),
        ]
        
        update_job = bigquery_client.query(update_query, job_config=bigquery.QueryJobConfig(
            query_parameters=query_params
        ))
        update_job.result()
        print(f"Updated user {user_id} in {table_id}.")
    else:
        # Insert new user data
        insert_data = [doc_data]
        errors = bigquery_client.insert_rows_json(table_ref, insert_data)
        if errors:
            for err in errors:
                print(f"BigQuery Error: {err}")
        else:
            print(f"Successfully inserted data into {table_id}.")

def firestore_listener(doc_snapshot, changes, error):
    if error:
        print(f"Error: {error}")
        return

    for change in changes:
        doc_data = change.document.to_dict()
        doc_data["user_id"] = change.document.id
        # Update or insert user in BigQuery
        update_or_insert_user(doc_data)

# Check and create the BigQuery table if it doesn't exist
check_and_create_table()

# Start listening for changes
collection_ref.on_snapshot(firestore_listener)

print("Listening for changes in Firestore collection...")

# Keep the script running to listen for changes
while True:
    time.sleep(10)
