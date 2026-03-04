# 🔧 Query Parameters Guide - How to Configure Endpoints with Params

## **Your Issue: 401 Error with Query Parameters**

### **Problem**
You're getting a **401 Unauthorized** error when testing your endpoint, but the same request works in Postman.

**Your Endpoint:**
```
GET https://hrsautl9-is.amer.reisystems.com/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ
```

### **Root Causes**

1. **Query parameters in Path field** - The system doesn't have a dedicated query params field yet
2. **Authentication mismatch** - Bearer token might not be passed correctly
3. **Headers missing** - Postman shows 7 headers, but you only configured Content-Type

---

## **Current Workaround (Until Query Params Field Added)**

### **Option 1: Include Query Params in Path** ✅

**How to configure:**

1. **Name**: `DSS-Terms And Conditions`
2. **Method**: `GET`
3. **Base URL**: `https://hrsautl9-is.amer.reisystems.com`
4. **Path**: `/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ`
   - ✅ Include the `?` and all query parameters
5. **Auth Type**: `Bearer Token`
6. **Auth Token**: `<your-actual-token>` (copy from Postman)
7. **Headers (JSON)**:
   ```json
   {
     "Content-Type": "application/json",
     "Accept": "application/json"
   }
   ```

**Important:** Make sure your Bearer Token is:
- ✅ Current and not expired
- ✅ Exactly the same as in Postman
- ✅ Has proper permissions for this endpoint

### **Option 2: Use Dynamic Parameters in Path**

For scenarios where the parameter value changes:

**Path**: `/EDIS.Api/api/TermsAndConditions?lastPullDate={{timestamp}}`

Then in your test scenario's request body configuration, you can replace `{{timestamp}}` with actual values.

---

## **Why You're Getting 401 Error**

### **Possible Reasons:**

#### **1. Token Expiration**
Bearer tokens typically expire. Your Postman token might be fresh, but the one in the platform might be old.

**Solution:**
- Copy the EXACT token from Postman
- Paste it into the Auth Token field
- Test connection immediately

#### **2. Missing Headers**
Postman shows **7 headers**, but you only configured Content-Type.

**What Postman sends:**
```
:status: 200
content-length: 6132
content-type: application/json; charset=utf-8
server: Microsoft-IIS/10.0
x-powered-by: ASP.NET
strict-transport-security: max-age=31536000; includeSubDomains
date: Tue, 24 Feb 2026 14:48:24 GMT
```

**What you should configure:**
```json
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

The other headers (server, date, etc.) are response headers, not request headers.

#### **3. URL Encoding Issues**
Your query parameter value contains special characters: `2026-01-24T02:50:59.318962TZ`

The `:` characters might need URL encoding.

**Encoded version:**
```
/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02%3A50%3A59.318962TZ
```

Try both encoded and non-encoded versions.

---

## **Step-by-Step: Fix Your 401 Error**

### **Step 1: Get Fresh Token from Postman**

1. Open Postman
2. Go to your working request
3. Click on "Authorization" tab
4. Copy the Bearer Token value
5. Make sure it's the FULL token (they can be very long)

### **Step 2: Configure Endpoint Correctly**

```
Name: DSS-Terms And Conditions
Method: GET
Base URL: https://hrsautl9-is.amer.reisystems.com
Path: /EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ
Auth Type: Bearer Token
Auth Token: <paste-full-token-here>
Expected Status: 200
Max Response Time: 2000
Timeout: 5000
Headers (JSON):
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

### **Step 3: Test Connection**

1. Click **"🔌 Test Connection"** button
2. Check the response:
   - ✅ Status 200 = Success
   - ❌ Status 401 = Token issue
   - ❌ Status 403 = Permission issue
   - ❌ Status 404 = URL wrong

### **Step 4: Debug Based on Result**

**If still 401:**
- Token is expired or invalid
- Token doesn't have permission for this endpoint
- Token format is wrong (should be just the token, not "Bearer <token>")

**If 403:**
- Token is valid but doesn't have access
- Check API permissions

**If 404:**
- URL is wrong
- Check Base URL + Path combination

**If 200:**
- ✅ Success! Click "Create" to save endpoint

---

## **Common Mistakes**

### **❌ Mistake 1: Including "Bearer" in Token Field**

**Wrong:**
```
Auth Type: Bearer Token
Auth Token: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Correct:**
```
Auth Type: Bearer Token
Auth Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The system automatically adds "Bearer" prefix.

### **❌ Mistake 2: Wrong Headers Format**

**Wrong:**
```
Content-Type: application/json
```

**Correct:**
```json
{
  "Content-Type": "application/json"
}
```

Must be valid JSON object.

### **❌ Mistake 3: Expired Token**

Bearer tokens expire. If your Postman request worked yesterday but the platform fails today, get a fresh token.

### **❌ Mistake 4: Query Params Not URL Encoded**

**If special characters in params:**
```
Before: ?lastPullDate=2026-01-24T02:50:59.318962TZ
After:  ?lastPullDate=2026-01-24T02%3A50%3A59.318962TZ
```

---

## **Future Enhancement: Query Parameters Field**

I'll add a dedicated **Query Parameters** field to make this easier:

**Planned UI:**
```
Path: /EDIS.Api/api/TermsAndConditions

Query Parameters (JSON):
{
  "lastPullDate": "2026-01-24T02:50:59.318962TZ"
}
```

The system will automatically construct the full URL.

---

## **Testing Checklist**

Before clicking "Create", verify:

- [ ] Base URL is correct (no trailing slash)
- [ ] Path includes query parameters with `?`
- [ ] Auth Type is "Bearer Token"
- [ ] Auth Token is fresh (copied from working Postman request)
- [ ] Headers are valid JSON
- [ ] Expected Status is 200
- [ ] Click "Test Connection" shows success

---

## **Example: Your Exact Configuration**

Based on your Postman screenshot:

```javascript
{
  "name": "DSS-Terms And Conditions",
  "method": "GET",
  "base_url": "https://hrsautl9-is.amer.reisystems.com",
  "path": "/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ",
  "auth_type": "bearer",
  "auth_token": "<YOUR_TOKEN_FROM_POSTMAN>",
  "headers": "{\"Content-Type\":\"application/json\",\"Accept\":\"application/json\"}",
  "expected_status": 200,
  "max_response_time_ms": 2000,
  "timeout_ms": 5000
}
```

**Replace `<YOUR_TOKEN_FROM_POSTMAN>` with your actual token!**

---

## **How to Get Token from Postman**

### **Method 1: From Authorization Tab**
1. Open your Postman request
2. Click "Authorization" tab
3. Copy the token value

### **Method 2: From Headers Tab**
1. Click "Headers" tab
2. Look for "Authorization" header
3. Copy everything AFTER "Bearer "
4. Example: `Authorization: Bearer abc123` → Copy `abc123`

### **Method 3: From Code Snippet**
1. Click "</>" icon in Postman
2. Select "cURL"
3. Find `-H "Authorization: Bearer <token>"`
4. Copy the token part

---

## **Troubleshooting 401 Errors**

### **Test 1: Verify Token Works**

Copy your Postman request as cURL:
```bash
curl -X GET "https://hrsautl9-is.amer.reisystems.com/EDIS.Api/api/TermsAndConditions?lastPullDate=2026-01-24T02:50:59.318962TZ" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

Run in terminal. If this works, token is valid.

### **Test 2: Check Token Expiration**

JWT tokens have expiration. Decode your token at jwt.io to check:
- `exp` field shows expiration timestamp
- Compare with current time

### **Test 3: Verify Permissions**

Your token might be valid but lack permissions for this specific endpoint. Check with your API admin.

---

## **Quick Fix Summary**

**To fix your 401 error:**

1. **Get fresh token from Postman** (most common fix)
2. **Paste EXACT token** (without "Bearer" prefix)
3. **Keep query params in Path field** (until dedicated field added)
4. **Add proper headers** as JSON object
5. **Test connection** before creating
6. **Check response** - should be 200 OK

**If still failing:**
- Token expired → Get new one
- Token invalid → Check format
- Token lacks permission → Contact API admin
- URL wrong → Verify Base URL + Path

---

## **Summary**

**Your Question:** How to add params when creating endpoint?

**Answer:** 
1. **Current method:** Include query parameters directly in the Path field with `?`
2. **Format:** `/api/endpoint?param1=value1&param2=value2`
3. **Your 401 error:** Most likely expired/invalid Bearer token
4. **Solution:** Copy fresh token from Postman, paste into Auth Token field
5. **Future:** Dedicated query parameters field will be added

**Try this now:**
1. Copy token from Postman
2. Edit your endpoint
3. Paste fresh token
4. Click "Test Connection"
5. Should get 200 OK

Let me know if you still get 401 after using a fresh token!
