import json
from google.cloud import firestore
from google.cloud import bigquery

project_id = 'simplitracapp'

firestore_client = firestore.Client()
bigquery_client = bigquery.Client(project=project_id)

dataset_id = 'simplitracapp.firestore_export'
table_id = 'simplitracapp.firestore_export.bi_viz'

def firestoreToBigQuery(event, context):
  """Triggered by a change to a Firestore document.
  Args:
      event: Event published by Cloud Firestore.
      context: Runtime metadata for the event.
  """
  snapshot = event.get('value')
  firestore_data = snapshot.get('data')

# Prepare data for BigQuery 
  data = {
      'user_id': firestore_data.get('user_id'),
      'email': firestore_data.get('email'),
      'google_id': firestore_data.get('google_id'),  # Assuming 'google_id' field exists
      'first_name': firestore_data.get('first_name'),
      'last_name': firestore_data.get('last_name'),
      'created_at': firestore_data.get('created_at'),  # Assuming 'created_at' is datetime
      'last_login': firestore_data.get('last_login'),  # Assuming 'last_login' is datetime
      'admin': firestore_data.get('admin'),  # Assuming 'admin' is boolean
      'transactions': firestore_data.get('transactions'),  # Assuming 'transactions' is a list
      'categories': firestore_data.get('categories'),  # Assuming 'categories' is a list
      'category_id': data.get('category_id'),
      'category_name': data.get('category_name'),
      'transaction_id': firestore_data.get('transaction_id'),  # Assuming 'transaction_id' exists
      'amount': firestore_data.get('amount'),
      'vendor': firestore_data.get('vendor'),
      'picture_id': firestore_data.get('picture_id'),
      'is_successful': firestore_data.get('is_successful'),
  }
  # Insert data into BigQuery table
  insert_row_to_bigquery(data)

def insert_row_to_bigquery(data):
  """
    Inserts a row into the BigQuery table.
  Args:
    data: A dictionary containing the data to be inserted.
  """
  try:
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    rows_to_insert = [data]
    table_ref.insert_rows(rows_to_insert)
    print(f"Inserted data into table: {table_ref}")
  except Exception as e:
    print(f"Error in inserting data to BigQuery: {e}")