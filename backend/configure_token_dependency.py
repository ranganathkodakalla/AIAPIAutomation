"""
Quick script to configure token dependency between EAAS-Connect Token and DSS-Terms And Conditions
"""
import sqlite3
import os

DB_PATH = "gs_api_test.db"

def configure_token_dependency():
    """Link DSS endpoint to EAAS token endpoint"""
    
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Find EAAS-Connect Token endpoint
        cursor.execute("SELECT id, name FROM api_endpoints WHERE name LIKE '%EAAS%Connect%Token%' OR name LIKE '%Token%'")
        token_endpoints = cursor.fetchall()
        
        if not token_endpoints:
            print("❌ EAAS-Connect Token endpoint not found!")
            print("Please create the EAAS-Connect Token endpoint first.")
            return
        
        print("Found token endpoints:")
        for ep_id, ep_name in token_endpoints:
            print(f"  - ID {ep_id}: {ep_name}")
        
        token_endpoint_id = token_endpoints[0][0]
        token_endpoint_name = token_endpoints[0][1]
        
        # Find DSS-Terms And Conditions endpoint
        cursor.execute("SELECT id, name FROM api_endpoints WHERE name LIKE '%DSS%Terms%' OR name LIKE '%TermsAndConditions%'")
        dss_endpoints = cursor.fetchall()
        
        if not dss_endpoints:
            print("❌ DSS-Terms And Conditions endpoint not found!")
            print("Please create the DSS-Terms And Conditions endpoint first.")
            return
        
        print("\nFound DSS endpoints:")
        for ep_id, ep_name in dss_endpoints:
            print(f"  - ID {ep_id}: {ep_name}")
        
        dss_endpoint_id = dss_endpoints[0][0]
        dss_endpoint_name = dss_endpoints[0][1]
        
        # Link them
        cursor.execute("""
            UPDATE api_endpoints 
            SET token_endpoint_id = ?,
                token_response_path = 'access_token'
            WHERE id = ?
        """, (token_endpoint_id, dss_endpoint_id))
        
        conn.commit()
        
        print(f"\n✅ Successfully configured token dependency!")
        print(f"   {dss_endpoint_name} (ID {dss_endpoint_id})")
        print(f"   ↓ will use tokens from")
        print(f"   {token_endpoint_name} (ID {token_endpoint_id})")
        print(f"\n🎯 Token will be extracted from response key: 'access_token'")
        print(f"⏱️  Tokens will be cached for 29 minutes (auto-refresh)")
        
        # Verify
        cursor.execute("SELECT token_endpoint_id, token_response_path FROM api_endpoints WHERE id = ?", (dss_endpoint_id,))
        result = cursor.fetchone()
        print(f"\n✓ Verification: token_endpoint_id={result[0]}, token_response_path={result[1]}")
        
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Configure Token Dependency")
    print("=" * 60)
    configure_token_dependency()
    print("\n" + "=" * 60)
    print("Next: Restart the application and run your tests!")
    print("=" * 60)
