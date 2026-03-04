"""
Database migration script to add missing columns to test_scenarios table
"""
import sqlite3
import os

DB_PATH = "gs_api_test.db"

def migrate_database():
    """Add missing columns to test_scenarios table"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(test_scenarios)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current columns in test_scenarios: {columns}")
        
        # Add missing columns
        if 'endpoint_id' not in columns:
            print("Adding endpoint_id column...")
            cursor.execute("ALTER TABLE test_scenarios ADD COLUMN endpoint_id INTEGER")
            print("✓ Added endpoint_id")
        
        if 'request_body' not in columns:
            print("Adding request_body column...")
            cursor.execute("ALTER TABLE test_scenarios ADD COLUMN request_body TEXT")
            print("✓ Added request_body")
        
        if 'expected_response' not in columns:
            print("Adding expected_response column...")
            cursor.execute("ALTER TABLE test_scenarios ADD COLUMN expected_response TEXT")
            print("✓ Added expected_response")
        
        if 'json_schema' not in columns:
            print("Adding json_schema column...")
            cursor.execute("ALTER TABLE test_scenarios ADD COLUMN json_schema TEXT")
            print("✓ Added json_schema")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Verify
        cursor.execute("PRAGMA table_info(test_scenarios)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nUpdated columns: {columns}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Database Migration Script")
    print("=" * 50)
    migrate_database()
