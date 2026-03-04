"""
Database migration to add business_rules column to mappings table
This allows users to define custom business rules for parsing and scenario generation
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
        # Check if column already exists
        cursor.execute("PRAGMA table_info(mappings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'business_rules' in columns:
            print("Column 'business_rules' already exists in mappings table")
            return
        
        # Add business_rules column
        print("Adding 'business_rules' column to mappings table...")
        cursor.execute("""
            ALTER TABLE mappings 
            ADD COLUMN business_rules TEXT
        """)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        print("   - Added 'business_rules' column to mappings table")
        print("\nYou can now add custom business rules when uploading Excel files.")
        
    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add Business Rules Column")
    print("=" * 60)
    migrate()
