# 🔐 Automatic Token Management - Complete Guide

## **Your Problem: Token Expiration & Manual Token Management**

You have a **token dependency chain**:
1. **EAAS-Connect Token** endpoint generates a bearer token (valid 1800 seconds = 30 minutes)
2. **DSS-Terms And Conditions** endpoint requires that token
3. Token expires quickly, causing tests to fail
4. Manual token copying is tedious and error-prone

---

## **Solution: Automatic Token Dependency System** ✅

The system now automatically:
- ✅ Fetches tokens from EAAS-Connect Token endpoint
- ✅ Caches tokens for reuse (up to 1800 seconds)
- ✅ Auto-refreshes tokens when expired
- ✅ Uses fresh tokens in DSS-Terms And Conditions tests
- ✅ No manual token copying needed!

---

## **How It Works**

### **Token Flow Diagram**

```
┌─────────────────────────────────────────────────────────┐
│ 1. Test Starts for "DSS-Terms And Conditions"          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. System checks: Does endpoint need a token?          │
│    → token_endpoint_id is set?                          │
└─────────────────────────────────────────────────────────┘
                        ↓ YES
┌─────────────────────────────────────────────────────────┐
│ 3. Check Token Cache                                    │
│    → Is there a valid cached token?                     │
└─────────────────────────────────────────────────────────┘
         ↓ NO                              ↓ YES
┌──────────────────────┐      ┌──────────────────────────┐
│ 4a. Fetch New Token  │      │ 4b. Use Cached Token     │
│ from EAAS-Connect    │      │ (Still valid)            │
│ Token endpoint       │      └──────────────────────────┘
└──────────────────────┘                   ↓
         ↓                                  │
┌──────────────────────┐                   │
│ 5. Cache Token       │                   │
│ Expires in 1800s     │                   │
└──────────────────────┘                   │
         ↓                                  │
         └──────────────┬───────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Make API Call to DSS-Terms And Conditions           │
│    with Bearer Token in Authorization header            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Get Response & Run Validations                      │
└─────────────────────────────────────────────────────────┘
```

---

## **Step-by-Step Configuration**

### **Step 1: Configure Token Endpoint (EAAS-Connect Token)**

This endpoint generates the bearer token.

**Configuration:**
```
Name: EAAS-Connect Token
Method: POST
Base URL: https://hrsautl9-is.amer.reisystems.com
Path: /EaasIdentityServer/connect/token

Auth Type: None
Auth Token: (leave empty)

Expected Status: 200
Max Response Time (ms): 2000
Timeout (ms): 5000

Headers (JSON):
{
  "Content-Type": "application/x-www-form-urlencoded"
}

Default Request Body (JSON):
client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials

Token Endpoint: None (this IS the token endpoint)
Token Response Path: access_token
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "expires_in": 1800,
  "token_type": "Bearer",
  "scope": "DSS_api EDIS_api ehb_id gs_api openid profile"
}
```

### **Step 2: Configure Dependent Endpoint (DSS-Terms And Conditions)**

This endpoint uses the token from Step 1.

**Configuration:**
```
Name: DSS-Terms And Conditions
Method: GET
Base URL: https://hrsautl9-is.amer.reisystems.com
Path: /EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ

Auth Type: Bearer Token (or leave as None, token will be auto-added)
Auth Token: (leave empty - will be auto-fetched)

Expected Status: 200
Max Response Time (ms): 2000
Timeout (ms): 5000

Headers (JSON):
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}

Token Endpoint: EAAS-Connect Token  ← SELECT THIS!
Token Response Path: access_token
```

**Key Settings:**
- **Token Endpoint:** Select "EAAS-Connect Token" from dropdown
- **Token Response Path:** `access_token` (the JSON key where token is found)

### **Step 3: Run Tests**

Now when you run tests for "DSS-Terms And Conditions":
1. System automatically calls EAAS-Connect Token endpoint
2. Extracts `access_token` from response
3. Caches it for 29 minutes (1740 seconds, 1 min before expiry)
4. Uses it in DSS-Terms And Conditions request
5. Gets actual response data!

---

## **Token Response Path Explained**

The **Token Response Path** tells the system where to find the token in the response JSON.

### **Example 1: Simple Path**

**Token Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "expires_in": 1800
}
```

**Token Response Path:** `access_token`

### **Example 2: Nested Path (Future Support)**

**Token Response:**
```json
{
  "data": {
    "auth": {
      "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
    }
  }
}
```

**Token Response Path:** `data.auth.token` (dot notation)

### **Example 3: Different Key Name**

**Token Response:**
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "expiry": 1800
}
```

**Token Response Path:** `token`

---

## **Token Caching Strategy**

### **Cache Duration**

- **Token expires in:** 1800 seconds (30 minutes)
- **Cache expires in:** 1740 seconds (29 minutes)
- **Refresh buffer:** 60 seconds before actual expiry

**Why the buffer?**
- Prevents using tokens that expire mid-request
- Ensures fresh tokens for all tests
- Reduces 401 authentication errors

### **Cache Reuse**

**Scenario 1: Multiple Tests in Quick Succession**
```
10:00:00 - Test 1 runs → Fetches new token
10:00:05 - Test 2 runs → Uses cached token
10:00:10 - Test 3 runs → Uses cached token
10:00:15 - Test 4 runs → Uses cached token
...
10:29:00 - Test N runs → Uses cached token
10:29:01 - Test N+1 runs → Fetches new token (cache expired)
```

**Scenario 2: Tests After Long Pause**
```
10:00:00 - Test 1 runs → Fetches new token
10:35:00 - Test 2 runs → Fetches new token (cache expired)
```

---

## **Frontend Configuration (Coming Soon)**

The frontend UI will be updated to include:

### **Endpoint Form - New Fields**

```
┌─────────────────────────────────────────────────────────┐
│ Token Endpoint (Optional)                               │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Select endpoint that provides bearer token...       │ │
│ │ ▼ EAAS-Connect Token                                │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Token Response Path                                     │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ access_token                                        │ │
│ └─────────────────────────────────────────────────────┘ │
│ (JSON key where token is found in response)            │
└─────────────────────────────────────────────────────────┘
```

### **How to Use (Manual Configuration for Now)**

Until the frontend is updated, configure via database or API:

**Option 1: Direct Database Update**
```sql
UPDATE api_endpoints 
SET token_endpoint_id = (SELECT id FROM api_endpoints WHERE name = 'EAAS-Connect Token'),
    token_response_path = 'access_token'
WHERE name = 'DSS-Terms And Conditions';
```

**Option 2: API Request**
```bash
curl -X PUT http://localhost:8000/api/endpoints/3 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DSS-Terms And Conditions",
    "environment_id": 1,
    "base_url": "https://hrsautl9-is.amer.reisystems.com",
    "path": "/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ",
    "method": "GET",
    "expected_status": 200,
    "timeout_ms": 5000,
    "max_response_time_ms": 2000,
    "headers": "{\"Content-Type\":\"application/json\"}",
    "token_endpoint_id": 2,
    "token_response_path": "access_token"
  }'
```

---

## **Troubleshooting**

### **Problem: Tests Still Showing All Pass (No Response Data)**

**Cause:** Token dependency not configured correctly.

**Solution:**
1. Verify `token_endpoint_id` is set for DSS endpoint
2. Check EAAS-Connect Token endpoint returns 200 OK
3. Verify `token_response_path` matches response JSON key
4. Check backend logs for token fetch messages

### **Problem: "Failed to fetch token" in Logs**

**Cause:** EAAS-Connect Token endpoint failing.

**Solution:**
1. Test EAAS-Connect Token endpoint manually
2. Verify client_id and client_secret are correct
3. Check Content-Type header is `application/x-www-form-urlencoded`
4. Ensure request body format is correct

### **Problem: Getting 401 Unauthorized**

**Cause:** Token not being added to request, or token invalid.

**Solution:**
1. Check backend logs: "Using auto-fetched token for..."
2. Verify token is in response: `access_token` key exists
3. Test token manually in Postman
4. Check token hasn't expired (1800 seconds)

### **Problem: Token Cached But Still Failing**

**Cause:** Cached token might be invalid or expired.

**Solution:**
1. Clear token cache:
   ```sql
   DELETE FROM token_cache;
   ```
2. Restart backend server
3. Run test again - will fetch fresh token

---

## **Database Schema**

### **api_endpoints Table (Updated)**

```sql
CREATE TABLE api_endpoints (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    environment_id INTEGER NOT NULL,
    base_url VARCHAR NOT NULL,
    method VARCHAR DEFAULT 'GET',
    path VARCHAR DEFAULT '/',
    auth_type VARCHAR,
    auth_token VARCHAR,
    headers TEXT,
    default_request_body TEXT,
    timeout_ms INTEGER DEFAULT 5000,
    expected_status INTEGER DEFAULT 200,
    max_response_time_ms INTEGER DEFAULT 2000,
    created_date DATETIME,
    token_endpoint_id INTEGER,  -- NEW: Points to token provider endpoint
    token_response_path VARCHAR DEFAULT 'access_token',  -- NEW: JSON path to token
    FOREIGN KEY (environment_id) REFERENCES environments(id),
    FOREIGN KEY (token_endpoint_id) REFERENCES api_endpoints(id)
);
```

### **token_cache Table (New)**

```sql
CREATE TABLE token_cache (
    id INTEGER PRIMARY KEY,
    endpoint_id INTEGER NOT NULL,  -- Which endpoint provided this token
    token VARCHAR NOT NULL,  -- The actual bearer token
    expires_at DATETIME NOT NULL,  -- When token expires
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endpoint_id) REFERENCES api_endpoints(id)
);
```

---

## **Benefits**

### **Before (Manual Token Management)**
❌ Copy token from EAAS-Connect Token response  
❌ Paste into DSS-Terms And Conditions endpoint config  
❌ Token expires after 30 minutes  
❌ Tests fail with 401 errors  
❌ Repeat process for every test session  
❌ No response data in test results  

### **After (Automatic Token Management)**
✅ System fetches tokens automatically  
✅ Tokens cached and reused for 29 minutes  
✅ Auto-refresh when expired  
✅ No manual copying needed  
✅ Tests always have valid tokens  
✅ Full response data in test results  

---

## **Advanced Use Cases**

### **Use Case 1: Multiple Endpoints Sharing Same Token**

```
EAAS-Connect Token (generates token)
    ↓
    ├─→ DSS-Terms And Conditions (uses token)
    ├─→ EDIS API (uses token)
    └─→ Another Endpoint (uses token)
```

All three endpoints can reference the same `token_endpoint_id`.

### **Use Case 2: Token Chain**

```
Auth Endpoint (generates auth token)
    ↓
Token Endpoint (uses auth token, generates API token)
    ↓
API Endpoint (uses API token)
```

Configure:
- Token Endpoint → token_endpoint_id = Auth Endpoint
- API Endpoint → token_endpoint_id = Token Endpoint

### **Use Case 3: Different Tokens for Different Environments**

```
DEV Environment:
- EAAS-Connect Token (DEV)
- DSS-Terms And Conditions (DEV) → uses DEV token

PROD Environment:
- EAAS-Connect Token (PROD)
- DSS-Terms And Conditions (PROD) → uses PROD token
```

Each environment has its own token endpoint and cache.

---

## **API Endpoints for Token Management**

### **Clear Token Cache**

```bash
DELETE http://localhost:8000/api/tokens/cache
```

Clears all cached tokens, forcing fresh fetch on next test.

### **View Token Cache (Future)**

```bash
GET http://localhost:8000/api/tokens/cache
```

Returns all cached tokens with expiration times.

### **Manual Token Refresh (Future)**

```bash
POST http://localhost:8000/api/tokens/refresh/{endpoint_id}
```

Forces a token refresh for specific endpoint.

---

## **Summary**

**Your Specific Configuration:**

1. **EAAS-Connect Token Endpoint:**
   - POST to `/EaasIdentityServer/connect/token`
   - Body: `client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials`
   - Returns: `{"access_token": "...", "expires_in": 1800}`

2. **DSS-Terms And Conditions Endpoint:**
   - GET to `/EDIS.Api/api/TermsAndConditions?lastPullDate=...`
   - Set `token_endpoint_id` to EAAS-Connect Token endpoint ID
   - Set `token_response_path` to `access_token`
   - System auto-fetches and uses token

3. **Result:**
   - ✅ No more manual token copying
   - ✅ Tokens auto-refresh every 30 minutes
   - ✅ Tests get actual response data
   - ✅ Validations work correctly

**Restart the application and run your tests - tokens will be managed automatically!** 🚀
