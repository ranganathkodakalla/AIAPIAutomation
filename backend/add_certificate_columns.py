"""
Migration script to add certificate authentication columns to api_endpoints table.
Run this once to add cert_path and cert_password columns.
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "gs_api_test.db"

def add_certificate_columns():
    """Add cert_path and cert_password columns to api_endpoints table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(api_endpoints)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'cert_path' not in columns:
            print("Adding cert_path column...")
            cursor.execute("ALTER TABLE api_endpoints ADD COLUMN cert_path TEXT")
            print("✓ cert_path column added")
        else:
            print("✓ cert_path column already exists")
        
        if 'cert_password' not in columns:
            print("Adding cert_password column...")
            cursor.execute("ALTER TABLE api_endpoints ADD COLUMN cert_password TEXT")
            print("✓ cert_password column added")
        else:
            print("✓ cert_password column already exists")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_certificate_columns()
