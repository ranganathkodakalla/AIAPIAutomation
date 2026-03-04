"""
Database migration to add expected_response column to ParsedField table
This allows Excel documents to include sample API responses for more accurate test scenario generation
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
        cursor.execute("PRAGMA table_info(parsed_fields)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'expected_response' in columns:
            print("Column 'expected_response' already exists in parsed_fields table")
            return
        
        # Add expected_response column
        print("Adding 'expected_response' column to parsed_fields table...")
        cursor.execute("""
            ALTER TABLE parsed_fields 
            ADD COLUMN expected_response TEXT
        """)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        print("   - Added 'expected_response' column to parsed_fields table")
        print("\nYou can now add Column G (Expected Response) to your Excel files.")
        
    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add Expected Response Column")
    print("=" * 60)
    migrate()
