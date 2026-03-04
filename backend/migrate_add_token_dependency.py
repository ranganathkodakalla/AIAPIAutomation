"""
Database migration script to add token dependency support to endpoints
- Adds token_endpoint_id column to api_endpoints table
- Adds token_cache table for storing and reusing tokens
"""
import sqlite3
import os

DB_PATH = "gs_api_test.db"

def migrate_database():
    """Add token dependency and caching support"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if token_endpoint_id column exists in api_endpoints
        cursor.execute("PRAGMA table_info(api_endpoints)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"Current columns in api_endpoints: {columns}")
        
        if 'token_endpoint_id' not in columns:
            print("Adding token_endpoint_id column to api_endpoints...")
            cursor.execute("ALTER TABLE api_endpoints ADD COLUMN token_endpoint_id INTEGER")
            print("✓ Added token_endpoint_id column")
        else:
            print("token_endpoint_id column already exists")
        
        if 'token_response_path' not in columns:
            print("Adding token_response_path column to api_endpoints...")
            cursor.execute("ALTER TABLE api_endpoints ADD COLUMN token_response_path VARCHAR")
            print("✓ Added token_response_path column")
        else:
            print("token_response_path column already exists")
        
        # Create token_cache table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='token_cache'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Creating token_cache table...")
            cursor.execute("""
                CREATE TABLE token_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint_id INTEGER NOT NULL,
                    token VARCHAR NOT NULL,
                    expires_at DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (endpoint_id) REFERENCES api_endpoints(id)
                )
            """)
            print("✓ Created token_cache table")
            
            # Add index for faster lookups
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_token_cache_endpoint_id ON token_cache(endpoint_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_token_cache_expires_at ON token_cache(expires_at)")
            print("✓ Created indexes on token_cache")
        else:
            print("token_cache table already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
        # Verify
        cursor.execute("PRAGMA table_info(api_endpoints)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\nUpdated api_endpoints columns: {columns}")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='token_cache'")
        if cursor.fetchone():
            print("✓ token_cache table verified")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration - Add Token Dependency Support")
    print("=" * 60)
    migrate_database()
