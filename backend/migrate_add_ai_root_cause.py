"""
Database migration to add AI root cause analysis fields
Adds root_cause_category, suggested_action, ai_confidence to validation_results
Creates root_cause_cache table for caching AI analyses
"""
import sqlite3
from pathlib import Path

def migrate():
    db_path = Path(__file__).parent / "gs_api_test.db"
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist in validation_results
        cursor.execute("PRAGMA table_info(validation_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        changes_made = []
        
        # Add root_cause_category if not exists
        if 'root_cause_category' not in columns:
            print("Adding 'root_cause_category' column to validation_results...")
            cursor.execute("""
                ALTER TABLE validation_results 
                ADD COLUMN root_cause_category TEXT
            """)
            changes_made.append("Added 'root_cause_category' column")
        
        # Add suggested_action if not exists
        if 'suggested_action' not in columns:
            print("Adding 'suggested_action' column to validation_results...")
            cursor.execute("""
                ALTER TABLE validation_results 
                ADD COLUMN suggested_action TEXT
            """)
            changes_made.append("Added 'suggested_action' column")
        
        # Add ai_confidence if not exists
        if 'ai_confidence' not in columns:
            print("Adding 'ai_confidence' column to validation_results...")
            cursor.execute("""
                ALTER TABLE validation_results 
                ADD COLUMN ai_confidence INTEGER
            """)
            changes_made.append("Added 'ai_confidence' column")
        
        # Check if root_cause_cache table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='root_cause_cache'
        """)
        
        if not cursor.fetchone():
            print("Creating 'root_cause_cache' table...")
            cursor.execute("""
                CREATE TABLE root_cause_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE NOT NULL,
                    category TEXT,
                    explanation TEXT,
                    suggested_action TEXT,
                    confidence INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX idx_cache_key ON root_cause_cache(cache_key)
            """)
            changes_made.append("Created 'root_cause_cache' table")
        
        if changes_made:
            conn.commit()
            print("\n✅ Migration completed successfully!")
            for change in changes_made:
                print(f"   - {change}")
            print("\nAI Root Cause Analysis is now ready to use!")
        else:
            print("✓ All AI root cause fields already exist. No migration needed.")
        
    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: AI Root Cause Analysis")
    print("=" * 60)
    migrate()
