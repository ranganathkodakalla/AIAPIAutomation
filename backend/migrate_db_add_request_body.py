"""
Database migration script to add default_request_body column to api_endpoints table
"""
import sqlite3
import os

DB_PATH = "gs_api_test.db"

def migrate_database():
    """Add default_request_body column to api_endpoints table"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(api_endpoints)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current columns in api_endpoints: {columns}")
        
        # Add missing column
        if 'default_request_body' not in columns:
            print("Adding default_request_body column...")
            cursor.execute("ALTER TABLE api_endpoints ADD COLUMN default_request_body TEXT")
            print("✓ Added default_request_body")
        else:
            print("Column default_request_body already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Verify
        cursor.execute("PRAGMA table_info(api_endpoints)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nUpdated columns: {columns}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Database Migration Script - Add Request Body")
    print("=" * 50)
    migrate_database()
