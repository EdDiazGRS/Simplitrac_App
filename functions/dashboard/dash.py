import json
from google.cloud import firestore
from google.cloud import bigquery

project_id = 'simplitracapp' #for GCP
dataset_id = 'firestore_export' #for BigQuery dataset
table_id = 'bi_viz' #for BigQuery Table

#Creating clients to interact with firestore and bigquery
firestore_client = firestore.Client()
bigquery_client = bigquery.Client(project=project_id)

#bigquery schema defintiions
schema = [
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("email", "STRING"),
    bigquery.SchemaField("first_name", "STRING"),
    bigquery.SchemaField("last_name", "STRING"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("last_login", "TIMESTAMP"),
    bigquery.SchemaField("admin", "BOOLEAN"),
    bigquery.SchemaField("transactions", "RECORD", mode="REPEATED", fields=[
        bigquery.SchemaField("transaction_id", "STRING"),
        bigquery.SchemaField("amount", "FLOAT"),
        bigquery.SchemaField("vendor", "STRING"),
        bigquery.SchemaField("is_successful", "BOOLEAN"),
    ]),
    bigquery.SchemaField("categories", "STRING", mode="REPEATED"),
    bigquery.SchemaField("category_id", "STRING"),
    bigquery.SchemaField("category_name", "STRING"),
    bigquery.SchemaField("picture_id", "STRING"),
]

def create_table_if_not_exists():
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    try:
        table = bigquery_client.get_table(table_ref)
        if len(table.schema) == 0:
            print(f"Table {table_id} exists but has no schema. Updating schema.")
            table.schema = schema
            bigquery_client.update_table(table, ['schema'])
            print(f"Updated schema for table {table.project}.{table.dataset_id}.{table.table_id}")
        else:
            print(f"Table {table_id} already exists with a schema.")
    except NotFound: #temp fix for now # type: ignore
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

def firestoreToBigQuery(event, context):
    """Triggered by a change to a Firestore document."""
    print("Function started")
    print("Event: ", json.dumps(event))
    
    if 'value' not in event:
        print("No 'value' key in event.")
        return
    
    snapshot = event.get('value')
    if not snapshot:
        print("No snapshot data found.")
        return

    firestore_data = snapshot.get('fields')
    if not firestore_data:
        print("No Firestore data found.")
        return

    print("Firestore data:", firestore_data)

    # Prepare data for BigQuery
    print("Preparing data for BigQuery")
    data = {
        'user_id': firestore_data.get('user_id', {}).get('stringValue', None),
        'google_id': firestore_data.get('google_id', {}).get('stringValue', None),
        'email': firestore_data.get('email', {}).get('stringValue', None),
        'f_name': firestore_data.get('f_name', {}).get('stringValue', None),
        'l_name': firestore_data.get('l_name', {}).get('stringValue', None),
        'created_at': firestore_data.get('created_at', {}).get('timestampValue', None),
        'last_login': firestore_data.get('last_login', {}).get('timestampValue', None),
        'admin': firestore_data.get('admin', {}).get('booleanValue', None),
        'categories': prepare_categories(firestore_data.get('Category', {}).get('arrayValue', {}).get('values', [])),
        'transactions': prepare_transactions(firestore_data.get('Transaction', {}).get('arrayValue', {}).get('values', [])),
        # For future expansion
        'picture': firestore_data.get('Picture', {}).get('blobValue', None),  # Adjust as per Firestore storage of blob data
        'coordinates': firestore_data.get('coordinates', {}).get('geoPointValue', None),  # Adjust as per Firestore storage of geojson
    }

    print("Data prepared:", data)

    # Ensure the table exists before inserting
    create_table_if_not_exists()

    # Insert data into BigQuery table
    print("Inserting data into BigQuery")
    insert_row_to_bigquery(data)

    print("Function completed")

def prepare_categories(categories_data):
    categories = []
    for category in categories_data:
        category_data = {
            'category_id': category.get('mapValue', {}).get('fields', {}).get('category_id', {}).get('stringValue', None),
            'category_name': category.get('mapValue', {}).get('fields', {}).get('category_name', {}).get('stringValue', None),
        }
        categories.append(category_data)
    return categories

def prepare_transactions(transactions_data):
    transactions = []
    for transaction in transactions_data:
        transaction_data = {
            'transaction_id': transaction.get('mapValue', {}).get('fields', {}).get('transaction_id', {}).get('stringValue', None),
            'created_at': transaction.get('mapValue', {}).get('fields', {}).get('created_at', {}).get('timestampValue', None),
            'amount': transaction.get('mapValue', {}).get('fields', {}).get('amount', {}).get('doubleValue', None),
            'vendor': transaction.get('mapValue', {}).get('fields', {}).get('vendor', {}).get('stringValue', None),
            'category_id': transaction.get('mapValue', {}).get('fields', {}).get('category_id', {}).get('stringValue', None),
            'is_successful': transaction.get('mapValue', {}).get('fields', {}).get('is_successful', {}).get('booleanValue', None),
            'recheck': transaction.get('mapValue', {}).get('fields', {}).get('recheck', {}).get('booleanValue', None),
        }
        transactions.append(transaction_data)
    return transactions

def insert_row_to_bigquery(data):
    """
    Inserts a row into the BigQuery table.
    Args:
        data: A dictionary containing the data to be inserted.
    """
    try:
        table_ref = bigquery_client.dataset(dataset_id).table(table_id)
        rows_to_insert = [data]
        errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
        if errors == []:
            print(f"Inserted data into table: {table_ref}")
        else:
            print(f"Errors in inserting data to BigQuery: {errors}")
    except Exception as e:
        print(f"Error in inserting data to BigQuery: {e}")

# Test the function with a sample event (this part is for testing purpose and should be removed in production)
if __name__ == "__main__":
    event = {
        'value': {
            'fields': {
                'user_id': {'stringValue': '123'},
                'email': {'stringValue': 'test@example.com'},
                'google_id': {'stringValue': 'google123'},
                'first_name': {'stringValue': 'John'},
                'last_name': {'stringValue': 'Doe'},
                'created_at': {'timestampValue': '2021-01-01T00:00:00Z'},
                'last_login': {'timestampValue': '2021-06-01T00:00:00Z'},
                'admin': {'booleanValue': True},
                'transactions': {'arrayValue': {'values': []}},
                'categories': {'arrayValue': {'values': []}},
                'category_id': {'stringValue': 'cat123'},
                'category_name': {'stringValue': 'Groceries'},
                'transaction_id': {'stringValue': 'trans123'},
                'amount': {'doubleValue': 100.0},
                'vendor': {'stringValue': 'VendorName'},
                'picture_id': {'stringValue': 'pic123'},
                'is_successful': {'booleanValue': True},
            }
        }
    }
    context = None
    firestoreToBigQuery(event, context)