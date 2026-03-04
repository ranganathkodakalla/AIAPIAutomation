#!/usr/bin/env python3
"""
Fix DSS endpoint URL to match the correct domain
"""

import sqlite3

def fix_dss_endpoint():
    """Update DSS endpoint URL"""
    
    db_path = "gs_api_test.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current DSS endpoint
        cursor.execute("SELECT id, name, base_url, path FROM api_endpoints WHERE id = 4")
        row = cursor.fetchone()
        
        if row:
            print(f"Current DSS Endpoint:")
            print(f"  ID: {row[0]}")
            print(f"  Name: {row[1]}")
            print(f"  Base URL: {row[2]}")
            print(f"  Path: {row[3]}")
            print(f"  Full URL: {row[2]}{row[3]}")
            print()
            
            # Update to correct domain
            new_base_url = "https://hrsaut19-is.amer.reisystems.com"
            
            cursor.execute("""
                UPDATE api_endpoints 
                SET base_url = ? 
                WHERE id = 4
            """, (new_base_url,))
            
            conn.commit()
            
            # Verify update
            cursor.execute("SELECT id, name, base_url, path FROM api_endpoints WHERE id = 4")
            row = cursor.fetchone()
            
            print(f"✅ Updated DSS Endpoint:")
            print(f"  ID: {row[0]}")
            print(f"  Name: {row[1]}")
            print(f"  Base URL: {row[2]}")
            print(f"  Path: {row[3]}")
            print(f"  Full URL: {row[2]}{row[3]}")
        else:
            print("❌ DSS endpoint (ID: 4) not found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_dss_endpoint()
