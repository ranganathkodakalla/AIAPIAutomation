# 📝 How to Add Body Parameters from Postman

## **Your Question: How to add body parameters from Postman to this tool?**

Looking at your Postman screenshot, you're using **x-www-form-urlencoded** body parameters for a POST request. Here's exactly how to configure this in the tool.

---

## **Your Postman Request**

```
POST https://hrsautl9-is.amer.reisystems.com/EaasIdentityServer/connect/token

Content-Type: application/x-www-form-urlencoded

Body Parameters:
- client_id: gs_client
- client_secret: grantsolutionsclient
- grant_type: client_credentials
```

---

## **How to Configure in the Tool**

### **Step-by-Step Configuration**

1. **Click "New Endpoint"** or **Edit existing endpoint**

2. **Fill in Basic Details:**
   ```
   Name: EAAS-Connect Token
   Method: POST
   Base URL: https://hrsautl9-is.amer.reisystems.com
   Path: /EaasIdentityServer/connect/token
   ```

3. **Set Headers:**
   ```json
   {
     "Content-Type": "application/x-www-form-urlencoded"
   }
   ```
   ⚠️ **Important:** This header tells the system to send form data, not JSON

4. **Add Body Parameters:**
   
   In the **"Default Request Body (JSON)"** field, enter:
   ```
   client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
   ```
   
   ✅ **This is the URL-encoded format** - parameters separated by `&`

5. **Set Other Fields:**
   ```
   Auth Type: None
   Auth Token: (leave empty)
   Expected Status: 200
   Max Response Time (ms): 2000
   Timeout (ms): 5000
   ```

6. **Click "Test Connection"** to verify it works

7. **Click "Create"** or **"Update"** to save

---

## **Complete Configuration Example**

Here's what your endpoint form should look like:

```
┌─────────────────────────────────────────────────────────┐
│ Name: EAAS-Connect Token                                │
├─────────────────────────────────────────────────────────┤
│ Method: POST                                            │
├─────────────────────────────────────────────────────────┤
│ Base URL: https://hrsautl9-is.amer.reisystems.com      │
├─────────────────────────────────────────────────────────┤
│ Path: /EaasIdentityServer/connect/token                │
├─────────────────────────────────────────────────────────┤
│ Auth Type: None                                         │
├─────────────────────────────────────────────────────────┤
│ Expected Status: 200                                    │
├─────────────────────────────────────────────────────────┤
│ Max Response Time (ms): 2000                            │
├─────────────────────────────────────────────────────────┤
│ Timeout (ms): 5000                                      │
├─────────────────────────────────────────────────────────┤
│ Headers (JSON):                                         │
│ {"Content-Type":"application/x-www-form-urlencoded"}    │
├─────────────────────────────────────────────────────────┤
│ Default Request Body (JSON):                            │
│ client_id=gs_client&client_secret=grantsolutions       │
│ client&grant_type=client_credentials                    │
└─────────────────────────────────────────────────────────┘
```

---

## **Different Body Parameter Formats**

### **Format 1: URL-Encoded (Form Data)** ✅ **Your Case**

**Postman:**
```
Body Type: x-www-form-urlencoded
Parameters:
  client_id: gs_client
  client_secret: grantsolutionsclient
  grant_type: client_credentials
```

**In Tool:**
```
Headers: {"Content-Type": "application/x-www-form-urlencoded"}
Body: client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

### **Format 2: JSON Body**

**Postman:**
```
Body Type: raw (JSON)
{
  "username": "admin",
  "password": "secret123"
}
```

**In Tool:**
```
Headers: {"Content-Type": "application/json"}
Body: 
{
  "username": "admin",
  "password": "secret123"
}
```

### **Format 3: Form Data with Files**

**Postman:**
```
Body Type: form-data
Parameters:
  file: [file upload]
  description: "My document"
```

**In Tool:**
```
Headers: {"Content-Type": "multipart/form-data"}
Body: (Not fully supported yet - use JSON or URL-encoded)
```

---

## **Common Mistakes & Fixes**

### **❌ Mistake 1: Wrong Header**

**Wrong:**
```json
{"Content-Type": "application/json"}
```

**Correct:**
```json
{"Content-Type": "application/x-www-form-urlencoded"}
```

**Why:** JSON header will send data as JSON object, not form parameters

### **❌ Mistake 2: JSON Format in Body**

**Wrong:**
```json
{
  "client_id": "gs_client",
  "client_secret": "grantsolutionsclient"
}
```

**Correct:**
```
client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

**Why:** With form-urlencoded header, body must be URL-encoded string

### **❌ Mistake 3: Missing `&` Separator**

**Wrong:**
```
client_id=gs_client client_secret=grantsolutionsclient
```

**Correct:**
```
client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

**Why:** Parameters must be separated by `&` character

### **❌ Mistake 4: Spaces in Values**

**Wrong:**
```
client_id=gs client&grant_type=client credentials
```

**Correct:**
```
client_id=gs_client&grant_type=client_credentials
```

**Or URL-encode spaces:**
```
client_id=gs%20client&grant_type=client%20credentials
```

---

## **How to Convert Postman Body to Tool Format**

### **Method 1: Manual Conversion**

**Postman Body:**
```
Key          | Value
-------------|------------------
client_id    | gs_client
client_secret| grantsolutionsclient
grant_type   | client_credentials
```

**Conversion:**
1. Take first parameter: `client_id=gs_client`
2. Add `&` separator
3. Add second parameter: `client_secret=grantsolutionsclient`
4. Add `&` separator
5. Add third parameter: `grant_type=client_credentials`

**Result:**
```
client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

### **Method 2: Copy from Postman Code Snippet**

1. In Postman, click **"<>"** (Code) button
2. Select **"cURL"**
3. Find the `--data` or `--data-urlencode` line
4. Copy the parameters
5. Paste into tool's body field

**Example cURL:**
```bash
curl --location 'https://hrsautl9-is.amer.reisystems.com/EaasIdentityServer/connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data 'client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials'
```

**Copy this part:**
```
client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

---

## **Testing Your Configuration**

### **Step 1: Click "Test Connection"**

After entering all details, click the **"🔌 Test Connection"** button.

### **Step 2: Check Response**

**Success (200 OK):**
```
✅ Connection successful! Status: 200, Time: 450ms

Response Body:
{
  "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Failure (400 Bad Request):**
```
⚠️ Status mismatch: Expected 200, Got 400

Response Body:
{
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
```

### **Step 3: Debug if Needed**

**If you get 400 error:**
- Check client_id and client_secret are correct
- Verify no extra spaces in values
- Ensure Content-Type header is set

**If you get 401 error:**
- Credentials are invalid
- Check values match Postman exactly

**If you get 404 error:**
- URL is wrong
- Check Base URL + Path combination

---

## **Special Characters in Parameters**

### **Characters That Need URL Encoding**

| Character | URL Encoded | Example |
|-----------|-------------|---------|
| Space | `%20` or `+` | `name=John%20Doe` |
| `&` | `%26` | `company=A%26B` |
| `=` | `%3D` | `formula=x%3D5` |
| `+` | `%2B` | `phone=%2B1234` |
| `#` | `%23` | `tag=%23important` |
| `?` | `%3F` | `query=what%3F` |

### **Example with Special Characters**

**Postman:**
```
Key: description
Value: This & that = something
```

**In Tool:**
```
description=This%20%26%20that%20%3D%20something
```

Or let the system handle it:
```
description=This & that = something
```
(System will auto-encode if needed)

---

## **Multiple Endpoints with Different Body Types**

You can create multiple endpoints with different body formats:

### **Endpoint 1: Token Request (Form Data)**
```
Name: Get Token
Method: POST
Headers: {"Content-Type": "application/x-www-form-urlencoded"}
Body: client_id=gs_client&client_secret=secret&grant_type=client_credentials
```

### **Endpoint 2: Create User (JSON)**
```
Name: Create User
Method: POST
Headers: {"Content-Type": "application/json"}
Body: {"username": "john", "email": "john@example.com"}
```

### **Endpoint 3: Get Data (No Body)**
```
Name: Get Users
Method: GET
Headers: {"Accept": "application/json"}
Body: (empty)
```

---

## **Using Body Parameters in Test Scenarios**

After creating your endpoint with body parameters:

### **Option 1: Use Default Body**

The endpoint's default body will be used automatically when running tests.

### **Option 2: Override in Scenario**

1. Click **"Configure"** on a test scenario
2. Select your endpoint
3. **Modify the request body** if needed:
   ```
   client_id=different_client&client_secret=different_secret&grant_type=client_credentials
   ```
4. Save and run

### **Option 3: Create Multiple Scenarios**

Create different scenarios with different body parameters:

**Scenario 1: Valid Credentials**
```
Body: client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
Expected: 200 OK with access_token
```

**Scenario 2: Invalid Client**
```
Body: client_id=invalid&client_secret=wrong&grant_type=client_credentials
Expected: 400 Bad Request with error
```

**Scenario 3: Missing Parameter**
```
Body: client_id=gs_client&grant_type=client_credentials
Expected: 400 Bad Request (missing client_secret)
```

---

## **Troubleshooting**

### **Problem: "Invalid JSON in request body" Error**

**Cause:** You entered URL-encoded format but didn't set the correct header.

**Solution:**
1. Set header: `{"Content-Type": "application/x-www-form-urlencoded"}`
2. Keep body as: `client_id=gs_client&client_secret=...`

### **Problem: Getting 400 Error**

**Cause:** Body format doesn't match what API expects.

**Solution:**
1. Check Postman's Content-Type header
2. Match it exactly in the tool
3. Use same body format as Postman

### **Problem: Parameters Not Received by API**

**Cause:** Wrong Content-Type or body format.

**Solution:**
1. Verify Content-Type header matches Postman
2. Check body format (URL-encoded vs JSON)
3. Test in Postman first, then copy exact format

---

## **Quick Reference**

### **For x-www-form-urlencoded (Your Case)**

```
Headers: {"Content-Type": "application/x-www-form-urlencoded"}
Body: param1=value1&param2=value2&param3=value3
```

### **For JSON**

```
Headers: {"Content-Type": "application/json"}
Body: {"param1": "value1", "param2": "value2"}
```

### **For Raw Text**

```
Headers: {"Content-Type": "text/plain"}
Body: Any text content here
```

---

## **Summary**

**To add body parameters from Postman:**

1. ✅ Copy the **Content-Type** header from Postman to tool's Headers field
2. ✅ If **x-www-form-urlencoded**: Format as `param1=value1&param2=value2`
3. ✅ If **JSON**: Format as `{"param1": "value1", "param2": "value2"}`
4. ✅ Click **"Test Connection"** to verify
5. ✅ Click **"Create"** to save

**Your specific configuration:**
```
Headers: {"Content-Type": "application/x-www-form-urlencoded"}
Body: client_id=gs_client&client_secret=grantsolutionsclient&grant_type=client_credentials
```

**That's it! The system will now send the body parameters exactly like Postman does.** 🚀
