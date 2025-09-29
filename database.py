import sqlite3
import json
from datetime import datetime

DATABASE = 'court_queries.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_number TEXT NOT NULL,
            year TEXT NOT NULL,
            response_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_query(case_type, case_number, year, response_data):
    """Save a query and its response to database"""
    conn = get_db_connection()
    cursor = conn.execute('''
        INSERT INTO queries (case_type, case_number, year, response_data)
        VALUES (?, ?, ?, ?)
    ''', (case_type, case_number, year, json.dumps(response_data)))
    query_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return query_id

def get_all_queries():
    """Get all saved queries"""
    conn = get_db_connection()
    queries = conn.execute('''
        SELECT id, case_type, case_number, year, response_data, created_at
        FROM queries ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    
    result = []
    for query in queries:
        result.append({
            'id': query['id'],
            'case_type': query['case_type'],
            'case_number': query['case_number'],
            'year': query['year'],
            'response_data': json.loads(query['response_data']),
            'created_at': query['created_at']
        })
    return result