# 📝 Custom Test Scenarios & Request Body Guide

## **Question 1: Where to Enter Request Body for API Endpoints?**

### **Answer: Two Places**

#### **Option 1: Default Request Body in Endpoint Configuration** ✅ NEW!

When creating/editing an endpoint (for POST/PUT/PATCH methods):

1. Go to **API Endpoints** tab
2. Click **"+ New Endpoint"** or **"Edit"** on existing endpoint
3. Select Method: **POST**, **PUT**, or **PATCH**
4. A new field appears: **"Default Request Body (JSON)"**
5. Enter your JSON request body:
   ```json
   {
     "agency": "HRSA",
     "programOffice": "HAB",
     "foaNumber": "HRSA-25-006"
   }
   ```
6. Click **"🔌 Test Connection"** - Uses this request body
7. Click **"Create"** or **"Update"** to save

**Use Case:** Default request body for testing the endpoint directly

---

#### **Option 2: Per Test Scenario** (Coming Soon)

When creating a test scenario:
- Each scenario can have its own custom request body
- Override the endpoint's default request body
- Test different payloads (happy path, edge cases, errors)

---

## **Question 2: How to Create Custom Test Scenarios?**

### **Current Method: Excel Upload + AI Generation**

**Steps:**
1. Upload Excel mapping file
2. Click "Generate Tests" 
3. AI creates scenarios automatically

**Limitation:** Can't manually create custom scenarios yet

---

### **NEW Feature: Manual Test Scenario Creation** 🎯

I'll add a **"+ Create Custom Scenario"** button that lets you:

#### **What You Can Configure:**

1. **Scenario Name**: e.g., "Happy Path - Valid FOA"
2. **Category**: Positive, Negative, Edge Case, Security
3. **Select Endpoint**: Choose from your configured endpoints
4. **Request Body**: Custom JSON for this specific test
5. **Expected Response**: What you expect to receive
6. **JSON Schema**: Optional validation schema
7. **Validations**: Select which validations to run
   - SCHEMA (required fields)
   - TYPE (data types)
   - STATUS_CODE (HTTP status)
   - RESPONSE_TIME (performance)
   - JSON_SCHEMA (structure)

#### **Example Custom Scenario:**

```json
{
  "name": "Test Invalid FOA Number",
  "category": "negative",
  "endpoint": "EDIS - POST /EDIS.Api/api/runbook/run",
  "request_body": {
    "agency": "HRSA",
    "programOffice": "HAB",
    "foaNumber": "INVALID-123"
  },
  "expected_response": {
    "errors": {
      "foaNumber": ["Invalid FOA number format"]
    }
  },
  "expected_status": 400,
  "validations": ["SCHEMA", "TYPE", "STATUS_CODE"]
}
```

---

## **Complete Workflow**

### **Workflow 1: Test Endpoint Directly**

```
1. Create Endpoint
   ├─ Name: "EDIS"
   ├─ Method: POST
   ├─ URL: https://hrsautl9-is.amer.reisystems.com
   ├─ Path: /EDIS.Api/api/runbook/run
   ├─ Headers: {"Content-Type": "application/json"}
   ├─ Auth: Bearer Token
   └─ Default Request Body: { "agency": "HRSA", ... }

2. Test Connection
   ├─ Click "🔌 Test Connection"
   ├─ Uses default request body
   ├─ Shows: Status 200, Response Time 176ms
   └─ View full response

3. Save Endpoint
   └─ Ready to use in test scenarios
```

---

### **Workflow 2: Create & Run Custom Test Scenarios**

```
1. Go to Test Scenarios Tab

2. Click "+ Create Custom Scenario"

3. Fill in Form:
   ├─ Name: "Happy Path - Valid FOA"
   ├─ Category: "Positive"
   ├─ Select Endpoint: "EDIS"
   ├─ Request Body: { custom JSON }
   ├─ Expected Response: { expected JSON }
   ├─ JSON Schema: { optional schema }
   └─ Select Validations: [✓ All]

4. Save Scenario

5. Run Test
   ├─ Click "Run" button
   ├─ Makes API call with request body
   ├─ Validates response
   ├─ Shows pass/fail results
   └─ AI root cause for failures

6. View Results
   ├─ Pass/Fail counts
   ├─ Response time
   ├─ Detailed validation results
   ├─ Compare expected vs actual
   └─ Export to CSV/JSON
```

---

## **Benefits of Custom Scenarios**

✅ **Test Specific Cases** - Create targeted tests for edge cases  
✅ **No Excel Required** - Build tests directly in UI  
✅ **Reusable** - Save and run scenarios repeatedly  
✅ **Version Control** - Track test changes over time  
✅ **Mix & Match** - Combine AI-generated + manual scenarios  
✅ **Quick Iteration** - Modify and retest instantly  

---

## **Example Use Cases**

### **Use Case 1: API Development Testing**

**Scenario:** You're developing a new API endpoint

1. Create endpoint with sample request body
2. Test connection to verify it works
3. Create custom scenarios:
   - Happy path with valid data
   - Missing required fields
   - Invalid data types
   - Boundary values
   - Security tests (SQL injection, XSS)

### **Use Case 2: Regression Testing**

**Scenario:** Ensure API still works after changes

1. Create scenarios for all critical paths
2. Run all scenarios with one click
3. Compare results with previous runs
4. Export results for reporting

### **Use Case 3: Integration Testing**

**Scenario:** Test multiple endpoints together

1. Create scenario for Endpoint A
2. Use response from A in request for Endpoint B
3. Validate end-to-end flow
4. Track performance across chain

---

## **Current Status**

✅ **Completed:**
- Default request body field in endpoint configuration
- Request body support in test connection
- Backend API ready for custom scenarios

🚧 **In Progress:**
- Manual test scenario creation UI
- Scenario builder form

📋 **Next Steps:**
1. Add "+ Create Custom Scenario" button
2. Build scenario creation form
3. Integrate with existing test execution
4. Test end-to-end workflow

---

## **How to Use Right Now**

### **For POST Endpoints:**

1. **Restart Application:**
   ```bash
   .\start.bat
   ```

2. **Create/Edit Endpoint:**
   - Go to API Endpoints tab
   - Select Method: POST/PUT/PATCH
   - Enter Default Request Body:
     ```json
     {
       "agency": "HRSA",
       "programOffice": "HAB",
       "foaNumber": "HRSA-25-006",
       "fiscalYear": "2025"
     }
     ```

3. **Test Connection:**
   - Click "🔌 Test Connection"
   - Should now work with request body! ✅
   - View response and status

4. **Save Endpoint:**
   - Click "Create" or "Update"
   - Endpoint ready for use

---

## **Coming Soon: Manual Scenario Builder**

I'm building a UI that will let you:
- Click "+ Create Custom Scenario"
- Fill in a form with all test details
- Save and run immediately
- No Excel or AI required

**ETA:** Next update! 🚀

---

## **Summary**

**Your Questions Answered:**

1. ✅ **Where to enter request body?**
   - In endpoint configuration (for POST/PUT/PATCH)
   - Shows up automatically when you select those methods
   - Used for testing the endpoint

2. ✅ **How to create custom test scenarios?**
   - Currently: Excel upload + AI generation
   - Coming soon: Manual scenario builder UI
   - Will support full customization

**Try it now:** Restart app and edit your EDIS endpoint to add request body!
