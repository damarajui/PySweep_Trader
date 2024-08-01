import os

import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

# PostgreSQL connection
def get_postgres_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

# Elasticsearch connection
def get_elasticsearch_client():
    es = Elasticsearch([os.getenv('ELASTICSEARCH_HOST')])
    return es

# Function to store data in PostgreSQL
def store_in_postgres(data, table_name):
    conn = get_postgres_connection()
    cur = conn.cursor()
    
    # Implement the logic to insert data into the specified table
    # This is a placeholder and should be adapted to your specific data structure
    columns = ', '.join(data.columns)
    values = ', '.join(['%s' for _ in data.columns])
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    
    for _, row in data.iterrows():
        cur.execute(insert_query, tuple(row))
    
    conn.commit()
    cur.close()
    conn.close()

# Function to store data in Elasticsearch
def store_in_elasticsearch(data, index_name):
    es = get_elasticsearch_client()
    
    # Implement the logic to insert data into Elasticsearch
    # This is a placeholder and should be adapted to your specific data structure
    for _, row in data.iterrows():
        es.index(index=index_name, body=row.to_dict())