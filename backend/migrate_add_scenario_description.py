"""
Database migration to add description column to test_scenarios table
This allows scenarios to have descriptive text explaining what the test validates
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
        cursor.execute("PRAGMA table_info(test_scenarios)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'description' in columns:
            print("Column 'description' already exists in test_scenarios table")
            return
        
        # Add description column
        print("Adding 'description' column to test_scenarios table...")
        cursor.execute("""
            ALTER TABLE test_scenarios 
            ADD COLUMN description TEXT
        """)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        print("   - Added 'description' column to test_scenarios table")
        print("\nScenarios will now include descriptions explaining what they test.")
        
    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add Scenario Description Column")
    print("=" * 60)
    migrate()
