#!/usr/bin/env python3
"""
Migration script to add selected_endpoint column to mappings table
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Add selected_endpoint column to mappings table"""
    
    # Database path
    db_path = "gs_api_test.db"
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found. Please ensure the database exists.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(mappings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'selected_endpoint' not in columns:
            print("Adding selected_endpoint column to mappings table...")
            
            # Add the column
            cursor.execute("""
                ALTER TABLE mappings 
                ADD COLUMN selected_endpoint TEXT
            """)
            
            conn.commit()
            print("✅ selected_endpoint column added successfully!")
            
            # Verify the column was added
            cursor.execute("PRAGMA table_info(mappings)")
            updated_columns = [column[1] for column in cursor.fetchall()]
            
            if 'selected_endpoint' in updated_columns:
                print("✅ Column verification successful!")
            else:
                print("❌ Column verification failed!")
                
        else:
            print("selected_endpoint column already exists in mappings table")
        
        # Show current mappings
        cursor.execute("SELECT id, filename, selected_endpoint FROM mappings")
        mappings = cursor.fetchall()
        
        if mappings:
            print(f"\nCurrent mappings ({len(mappings)}):")
            for mapping in mappings:
                print(f"  ID: {mapping[0]}, File: {mapping[1]}, Endpoint: {mapping[2] or 'None'}")
        else:
            print("\nNo mappings found in database")
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
