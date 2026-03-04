"""
Database migration script to add execution tracking support
- Adds test_executions table
- Adds execution_id column to validation_results table
"""
import sqlite3
import os

DB_PATH = "gs_api_test.db"

def migrate_database():
    """Add execution tracking tables and columns"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if test_executions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_executions'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Creating test_executions table...")
            cursor.execute("""
                CREATE TABLE test_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scenario_id INTEGER NOT NULL,
                    execution_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR,
                    total_validations INTEGER,
                    passed_validations INTEGER,
                    failed_validations INTEGER,
                    response_body TEXT,
                    expected_response TEXT,
                    response_time_ms INTEGER,
                    FOREIGN KEY (scenario_id) REFERENCES test_scenarios(id)
                )
            """)
            print("✓ Created test_executions table")
        else:
            print("test_executions table already exists")
        
        # Check if execution_id column exists in validation_results
        cursor.execute("PRAGMA table_info(validation_results)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current columns in validation_results: {columns}")
        
        # Add missing columns
        columns_to_add = {
            'execution_id': 'INTEGER',
            'validation_type': 'VARCHAR',
            'response_time_ms': 'INTEGER',
            'status_code': 'INTEGER'
        }
        
        for column_name, column_type in columns_to_add.items():
            if column_name not in columns:
                print(f"Adding {column_name} column to validation_results...")
                cursor.execute(f"ALTER TABLE validation_results ADD COLUMN {column_name} {column_type}")
                print(f"✓ Added {column_name} column")
            else:
                print(f"{column_name} column already exists")
        
        # Add foreign key index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_validation_results_execution_id ON validation_results(execution_id)")
        print("✓ Created index on execution_id")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Verify
        cursor.execute("PRAGMA table_info(validation_results)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nUpdated validation_results columns: {columns}")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_executions'")
        if cursor.fetchone():
            print("✓ test_executions table verified")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration - Add Execution Tracking")
    print("=" * 60)
    migrate_database()
