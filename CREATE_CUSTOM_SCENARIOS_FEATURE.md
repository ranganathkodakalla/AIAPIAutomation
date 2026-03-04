# ✅ Create Custom Scenarios Feature - Complete Guide

## **Overview**

You can now create test scenarios **manually** without uploading an Excel file! This feature lets you build custom API tests directly in the UI.

---

## **How to Use**

### **Step 1: Navigate to Test Scenarios Tab**

1. Open the application: `http://localhost:5000`
2. Go to **Test Scenarios** tab
3. You'll see a **"+ Create Custom Scenario"** button at the top

### **Step 2: Click "Create Custom Scenario"**

A modal will open with the following fields:

---

## **Form Fields**

### **1. Scenario Name** (Required)
- **Purpose**: Descriptive name for your test
- **Example**: "Happy Path - Valid FOA Submission"
- **Example**: "Negative Test - Missing Required Fields"
- **Example**: "Edge Case - Maximum Length Values"

### **2. Category** (Required)
Select from:
- **Positive (Happy Path)** - Valid data, expected to succeed
- **Negative (Error Cases)** - Invalid data, expected to fail
- **Edge Cases** - Boundary values, unusual inputs
- **Security Tests** - SQL injection, XSS, authentication tests
- **Custom** - Any other type

### **3. API Endpoint** (Required)
- **Purpose**: Select which endpoint to test
- **Dropdown shows**: All configured endpoints from API Endpoints tab
- **Format**: `Name - Method URL/Path`
- **Example**: `EDIS - POST https://hrsautl9-is.amer.reisystems.com/EDIS.Api/api/runbook/run`

### **4. Request Body (JSON)**
- **Purpose**: The JSON payload to send with the request
- **When to use**: For POST, PUT, PATCH methods
- **Format**: Valid JSON
- **Example**:
  ```json
  {
    "agency": "HRSA",
    "programOffice": "HAB",
    "foaNumber": "HRSA-25-006",
    "fiscalYear": "2025",
    "foaTitle": "Test FOA Title"
  }
  ```

### **5. Expected Response (JSON)** (Optional)
- **Purpose**: What you expect the API to return
- **Use for**: Response comparison feature
- **Format**: Valid JSON
- **Example**:
  ```json
  {
    "status": "success",
    "message": "FOA created successfully",
    "data": {
      "foaId": "12345"
    }
  }
  ```

### **6. JSON Schema** (Optional)
- **Purpose**: Validate the structure of the API response
- **Use for**: Complex validation rules
- **Format**: JSON Schema Draft 7
- **Example**:
  ```json
  {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "data": {
        "type": "object",
        "properties": {
          "foaId": {"type": "string"}
        },
        "required": ["foaId"]
      }
    },
    "required": ["status", "data"]
  }
  ```

---

## **Step 3: Create the Scenario**

1. Fill in all required fields (marked with red asterisk *)
2. Click **"Create Scenario"** button
3. Modal closes and scenario appears in the list
4. Scenario is saved to database immediately

---

## **Step 4: Run Your Custom Scenario**

Once created, your custom scenario works exactly like AI-generated scenarios:

1. **Click "Run"** button on the scenario
2. System will:
   - Make actual API call to the endpoint
   - Send the request body you defined
   - Perform all 5 validation types:
     - ✅ SCHEMA - Required fields
     - ✅ TYPE - Data types
     - ✅ STATUS_CODE - HTTP status
     - ✅ RESPONSE_TIME - Performance
     - ✅ JSON_SCHEMA - Structure validation
3. View results with pass/fail counts
4. See detailed validation results
5. Get AI root cause analysis for failures

---

## **Complete Example**

### **Scenario: Test Valid FOA Submission**

**Configuration:**
```
Name: Happy Path - Valid FOA
Category: Positive (Happy Path)
Endpoint: EDIS - POST /EDIS.Api/api/runbook/run

Request Body:
{
  "agency": "HRSA",
  "programOffice": "HAB",
  "foaNumber": "HRSA-25-006",
  "fiscalYear": "2025",
  "foaTitle": "Ryan White HIV/AIDS Program",
  "foaStatus": "Draft",
  "elements": {
    "DESCRIPTION": "Test description",
    "ELIGIBLE_APPLICANTS": "State governments",
    "ESTIMATED_POST_DATE": "2025-01-15"
  }
}

Expected Response:
{
  "success": true,
  "message": "FOA processed successfully"
}

JSON Schema:
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "message": {"type": "string"}
  },
  "required": ["success", "message"]
}
```

**What Happens When You Run It:**
1. POST request sent to EDIS endpoint
2. Request body included in the call
3. Response captured
4. Validations run:
   - ✅ Status code 200
   - ✅ Response time < 2000ms
   - ✅ JSON schema matches
   - ✅ All required fields present
5. Results displayed with pass/fail
6. Can compare expected vs actual response

---

## **Use Cases**

### **Use Case 1: Quick API Testing**

**Scenario**: You want to test a new endpoint quickly

1. Create endpoint in API Endpoints tab
2. Create custom scenario with sample data
3. Run and verify it works
4. No Excel file needed!

### **Use Case 2: Edge Case Testing**

**Scenario**: Test boundary values

```
Name: Edge Case - Maximum Field Lengths
Category: Edge Cases
Request Body:
{
  "foaTitle": "A".repeat(500),  // Max length
  "fiscalYear": "9999"          // Future year
}
```

### **Use Case 3: Negative Testing**

**Scenario**: Test error handling

```
Name: Negative - Missing Required Fields
Category: Negative (Error Cases)
Request Body:
{
  "agency": "HRSA"
  // Missing programOffice, foaNumber, etc.
}
Expected Response:
{
  "errors": {
    "programOffice": ["This field is required"],
    "foaNumber": ["This field is required"]
  }
}
```

### **Use Case 4: Security Testing**

**Scenario**: Test SQL injection

```
Name: Security - SQL Injection Test
Category: Security Tests
Request Body:
{
  "foaNumber": "'; DROP TABLE foas; --"
}
Expected Response:
{
  "error": "Invalid input"
}
```

---

## **Features**

### **✅ What You Can Do**

- Create unlimited custom scenarios
- Test any configured endpoint
- Define custom request bodies
- Set expected responses
- Add JSON schema validation
- Run scenarios individually or all at once
- View detailed results
- Compare expected vs actual responses
- Export results to CSV/JSON
- View execution history
- Get AI root cause analysis

### **✅ Integration with Existing Features**

Your custom scenarios work with **all existing features**:
- Request Builder (Configure button)
- Response Comparison
- Test History
- Export Results
- JSON Schema Validation
- AI Root Cause Analysis

---

## **Backend Implementation**

### **New API Endpoint**

**POST** `/api/scenarios/create`

**Request Body:**
```json
{
  "name": "Scenario Name",
  "category": "positive",
  "endpoint_id": 1,
  "request_body": "{...}",
  "expected_response": "{...}",
  "json_schema": "{...}"
}
```

**Response:**
```json
{
  "id": 123,
  "mapping_id": 1,
  "endpoint_id": 1,
  "name": "Scenario Name",
  "category": "positive",
  "status": "pending",
  "request_body": "{...}",
  "expected_response": "{...}",
  "json_schema": "{...}"
}
```

### **Auto-Created Mapping**

- Custom scenarios are linked to a special mapping: "Custom Scenarios"
- This mapping is auto-created on first custom scenario
- Keeps custom scenarios separate from Excel-generated ones

---

## **Frontend Implementation**

### **New Components**

**Create Custom Scenario Modal:**
- Full-screen modal with form
- JSON editors with syntax highlighting
- Endpoint dropdown
- Category selector
- Validation (required fields)
- Cancel/Create buttons

**Button Integration:**
- Added to Test Scenarios tab header
- Always visible (even with no scenarios)
- Blue button with "+" icon

---

## **Workflow Comparison**

### **Excel Upload Method**

```
1. Create Excel file with field mappings
2. Upload to platform
3. AI parses and classifies rules
4. AI generates test scenarios
5. Review and run scenarios
```

**Pros:** Bulk creation, AI-powered
**Cons:** Requires Excel, less control

### **Custom Scenario Method** ✨ NEW!

```
1. Click "Create Custom Scenario"
2. Fill in form with test details
3. Click "Create"
4. Run immediately
```

**Pros:** Quick, precise control, no Excel
**Cons:** Manual, one at a time

### **Best Practice: Use Both!**

- **Excel Upload**: For bulk test generation from requirements
- **Custom Scenarios**: For specific edge cases, quick tests, ad-hoc testing

---

## **Tips & Best Practices**

### **1. Naming Convention**

Use descriptive names that indicate:
- Test type (Happy Path, Negative, Edge Case)
- What's being tested
- Expected outcome

**Good Examples:**
- ✅ "Happy Path - Valid FOA with All Fields"
- ✅ "Negative - Missing Required Field: foaNumber"
- ✅ "Edge Case - Maximum Length foaTitle (500 chars)"

**Bad Examples:**
- ❌ "Test 1"
- ❌ "FOA Test"
- ❌ "Scenario"

### **2. JSON Formatting**

- Use proper JSON syntax (double quotes, no trailing commas)
- Format for readability (use line breaks)
- Validate JSON before creating scenario

### **3. Expected Response**

- Only include fields you want to validate
- Use for critical assertions
- Leave empty if you just want to check status code

### **4. JSON Schema**

- Start simple, add complexity as needed
- Use for structure validation, not exact values
- Reference: https://json-schema.org/

---

## **Troubleshooting**

### **"Create Scenario" button is disabled**

**Cause:** Required fields are missing

**Solution:** 
- Ensure Scenario Name is filled
- Ensure an Endpoint is selected

### **Scenario created but won't run**

**Cause:** Invalid JSON in request body

**Solution:**
- Check JSON syntax
- Validate at jsonlint.com
- Look for missing quotes, commas, brackets

### **No endpoints in dropdown**

**Cause:** No endpoints configured yet

**Solution:**
1. Go to API Endpoints tab
2. Create at least one endpoint
3. Return to Test Scenarios tab

---

## **Files Modified**

**Backend:**
- `backend/main.py` - Added `/api/scenarios/create` endpoint

**Frontend:**
- `frontend/src/EnhancedScenario1Tab.jsx` - Added modal and creation logic

---

## **Next Steps**

1. **Restart Application:**
   ```bash
   .\start.bat
   ```

2. **Create Your First Custom Scenario:**
   - Go to Test Scenarios tab
   - Click "+ Create Custom Scenario"
   - Fill in the form
   - Click "Create Scenario"
   - Click "Run" to test it!

3. **Build Your Test Suite:**
   - Create scenarios for happy paths
   - Add negative test cases
   - Test edge cases
   - Add security tests
   - Run all scenarios together

---

## **Summary**

✅ **No Excel Required** - Build tests directly in UI  
✅ **Full Control** - Define exact request/response  
✅ **Quick Testing** - Create and run in seconds  
✅ **All Features** - Works with history, export, comparison  
✅ **Flexible** - Combine with AI-generated scenarios  
✅ **Production Ready** - Fully integrated with existing system  

**You now have complete flexibility in how you create and manage your API test scenarios!** 🚀
