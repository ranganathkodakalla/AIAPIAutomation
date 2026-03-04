# 🤖 Enhanced AI Test Generation - Complete Guide

## **Overview**

The system now has **3 ways** to create test scenarios, with the AI generation enhanced to automatically create complete request/response JSON.

---

## **Method 1: AI-Generated Scenarios (Enhanced!)** ✨

### **How It Works**

1. **Upload Excel file** with field mappings (data types, validation rules)
2. **Click "Generate Tests"**
3. **AI automatically creates 3 complete scenarios:**
   - ✅ Happy Path with valid request body
   - ✅ Negative Test - Missing required field
   - ✅ Negative Test - Invalid data type
4. **Each scenario includes:**
   - Descriptive name
   - Category (positive/negative)
   - **Complete request body JSON** (automatically generated!)
   - **Expected response JSON** (automatically generated!)
   - Linked to endpoint (if available)

### **What AI Generates**

**Example Output:**

#### **Scenario 1: Happy Path - All Valid Fields**
```json
{
  "name": "Happy Path - All Valid Fields",
  "category": "positive",
  "request_body": {
    "agency": "HRSA",
    "programOffice": "HAB",
    "foaNumber": "HRSA-25-006",
    "fiscalYear": "2025",
    "foaTitle": "Ryan White HIV/AIDS Program"
  },
  "expected_response": {
    "success": true,
    "message": "FOA created successfully",
    "data": {
      "foaId": "12345"
    }
  }
}
```

#### **Scenario 2: Missing Required Field - fiscalYear**
```json
{
  "name": "Missing Required Field - fiscalYear",
  "category": "negative",
  "request_body": {
    "agency": "HRSA",
    "programOffice": "HAB",
    "foaNumber": "HRSA-25-006",
    "foaTitle": "Ryan White HIV/AIDS Program"
    // fiscalYear intentionally omitted
  },
  "expected_response": {
    "errors": {
      "fiscalYear": ["This field is required"]
    }
  }
}
```

#### **Scenario 3: Invalid Type - foaNumber**
```json
{
  "name": "Invalid Type - foaNumber as Integer",
  "category": "negative",
  "request_body": {
    "agency": "HRSA",
    "programOffice": "HAB",
    "foaNumber": 12345,  // Should be string, not integer
    "fiscalYear": "2025",
    "foaTitle": "Ryan White HIV/AIDS Program"
  },
  "expected_response": {
    "errors": {
      "foaNumber": ["Must be a string"]
    }
  }
}
```

### **How AI Decides What to Generate**

The AI analyzes your Excel field mappings:

**Input from Excel:**
```
Field Name: fiscalYear
Data Type: string
Required: true
Example: "2025"
Validation Rule: Must be 4-digit year
```

**AI Creates:**
1. **Happy Path**: Uses valid example value "2025"
2. **Missing Field Test**: Omits fiscalYear entirely
3. **Invalid Type Test**: Uses wrong type (e.g., integer 2025 instead of string "2025")

---

## **Method 2: Manual Custom Scenarios** 🎯

### **When to Use**
- You want full control over test data
- Testing specific edge cases
- Quick one-off tests
- No Excel file available

### **How to Create**
1. Click **"+ Create Custom Scenario"**
2. Fill in form:
   - Scenario name
   - Category
   - Select endpoint
   - **Manually write request body JSON**
   - **Manually write expected response JSON**
   - Optional: JSON schema
3. Click "Create Scenario"
4. Run immediately

---

## **Method 3: Configure Generated Scenarios** ⚙️

### **When to Use**
- AI generated scenarios but you want to adjust them
- Need to change request/response data
- Want to link to different endpoint

### **How to Configure**
1. After AI generates scenarios, click **"Configure"** button
2. Modal opens with:
   - Endpoint selector
   - Request body editor (pre-filled by AI)
   - Expected response editor (pre-filled by AI)
   - JSON schema editor
3. Edit as needed
4. Save changes

---

## **Complete Workflow**

### **Workflow 1: AI-Generated End-to-End Testing**

```
1. Upload Excel File
   ├─ Field: agency (string, required)
   ├─ Field: programOffice (string, required)
   ├─ Field: foaNumber (string, required)
   └─ Field: fiscalYear (string, required)

2. Click "Generate Tests"
   └─ AI analyzes fields and validation rules

3. AI Creates 3 Scenarios Automatically:
   
   Scenario 1: Happy Path
   ├─ Request: All fields with valid data
   ├─ Expected: Success response
   └─ Status: Ready to run
   
   Scenario 2: Missing Required Field
   ├─ Request: Missing fiscalYear
   ├─ Expected: Error response
   └─ Status: Ready to run
   
   Scenario 3: Invalid Data Type
   ├─ Request: foaNumber as integer
   ├─ Expected: Type error response
   └─ Status: Ready to run

4. Run All Scenarios
   ├─ Makes real API calls
   ├─ Validates responses
   ├─ Shows pass/fail results
   └─ AI root cause for failures

5. View Results
   ├─ Response comparison
   ├─ Execution history
   └─ Export to CSV/JSON
```

### **Workflow 2: Hybrid Approach (AI + Manual)**

```
1. Upload Excel → AI generates 3 base scenarios

2. Click "Configure" on each scenario
   └─ Adjust request/response as needed

3. Click "+ Create Custom Scenario"
   └─ Add edge cases AI didn't cover

4. Run all scenarios together
   └─ Mix of AI-generated + custom tests
```

---

## **AI Prompt Engineering**

### **What We Send to AI**

```json
{
  "fields": [
    {
      "field_name": "agency",
      "data_type": "string",
      "required": true,
      "example_value": "HRSA",
      "validation_rule": "Must be valid agency code"
    },
    {
      "field_name": "fiscalYear",
      "data_type": "string",
      "required": true,
      "example_value": "2025",
      "validation_rule": "Must be 4-digit year"
    }
  ]
}
```

### **What AI Returns**

```json
[
  {
    "name": "Happy Path - All Valid Fields",
    "category": "positive",
    "request_body": {
      "agency": "HRSA",
      "fiscalYear": "2025"
    },
    "expected_response": {
      "success": true
    },
    "expected_status": 200
  },
  {
    "name": "Missing Required Field - fiscalYear",
    "category": "negative",
    "request_body": {
      "agency": "HRSA"
    },
    "expected_response": {
      "errors": {
        "fiscalYear": ["This field is required"]
      }
    },
    "expected_status": 400
  },
  {
    "name": "Invalid Type - fiscalYear as Integer",
    "category": "negative",
    "request_body": {
      "agency": "HRSA",
      "fiscalYear": 2025
    },
    "expected_response": {
      "errors": {
        "fiscalYear": ["Must be a string"]
      }
    },
    "expected_status": 400
  }
]
```

---

## **Benefits of Enhanced AI Generation**

### **Before (Old System)**
❌ AI only generated scenario names  
❌ Had to manually write request JSON  
❌ Had to manually write expected response  
❌ Had to click "Configure" on every scenario  
❌ Time-consuming and error-prone  

### **After (Enhanced System)**
✅ AI generates complete request bodies  
✅ AI generates expected responses  
✅ AI uses realistic example values  
✅ Scenarios are **immediately runnable**  
✅ Can still configure if needed  
✅ Saves hours of manual work  

---

## **Example: Real-World Use Case**

### **Scenario: Testing FOA Submission API**

**Excel Upload Contains:**
- 15 fields (agency, programOffice, foaNumber, fiscalYear, etc.)
- 8 required fields
- 7 optional fields
- Various data types (string, integer, date, boolean)
- Validation rules for each field

**What Happens:**

1. **Upload Excel** → System parses 15 fields

2. **Click "Generate Tests"** → AI creates:
   
   **Scenario 1: Happy Path**
   ```json
   {
     "request_body": {
       "agency": "HRSA",
       "programOffice": "HAB",
       "foaNumber": "HRSA-25-006",
       "fiscalYear": "2025",
       "foaTitle": "Ryan White HIV/AIDS Program",
       "foaStatus": "Draft",
       "estimatedPostDate": "2025-01-15",
       "estimatedCloseDate": "2025-03-15",
       // ... all 15 fields with valid data
     }
   }
   ```
   
   **Scenario 2: Missing programOffice**
   ```json
   {
     "request_body": {
       "agency": "HRSA",
       // programOffice omitted
       "foaNumber": "HRSA-25-006",
       // ... other fields
     }
   }
   ```
   
   **Scenario 3: Invalid fiscalYear Type**
   ```json
   {
     "request_body": {
       "agency": "HRSA",
       "programOffice": "HAB",
       "foaNumber": "HRSA-25-006",
       "fiscalYear": 2025,  // Integer instead of string
       // ... other fields
     }
   }
   ```

3. **Click "Run All Scenarios"** → Immediate execution
   - No manual configuration needed
   - All 3 scenarios run against real API
   - Results show pass/fail
   - AI explains any failures

4. **Optional: Add More Custom Scenarios**
   - Edge case: Maximum length values
   - Edge case: Special characters
   - Security: SQL injection test
   - Performance: Large payload test

---

## **Configuration Options**

### **Endpoint Linking**

**Automatic (Default):**
- AI links scenarios to first available endpoint
- Works if you have one main endpoint

**Manual Override:**
- Click "Configure" on scenario
- Select different endpoint from dropdown
- Useful for multi-endpoint testing

### **Request Body Customization**

**AI-Generated (Default):**
- Uses example values from Excel
- Creates realistic test data
- Follows validation rules

**Manual Override:**
- Click "Configure"
- Edit request body JSON
- Add/remove fields
- Change values

### **Expected Response Customization**

**AI-Generated (Default):**
- Predicts success/error responses
- Based on validation rules
- Standard REST API patterns

**Manual Override:**
- Click "Configure"
- Edit expected response JSON
- Match your actual API responses
- Add specific error messages

---

## **Troubleshooting**

### **AI Doesn't Generate Request Bodies**

**Cause:** Azure OpenAI not configured

**Solution:**
1. Check `.env` file has:
   ```
   AZURE_OPENAI_ENDPOINT=https://...
   AZURE_OPENAI_API_KEY=...
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   ```
2. Restart backend server

### **Generated Request Bodies Are Empty**

**Cause:** AI response parsing failed

**Solution:**
- Check backend logs for AI response
- Verify field mappings have example values
- Try regenerating tests

### **Scenarios Generated But Can't Run**

**Cause:** No endpoint linked

**Solution:**
1. Go to API Endpoints tab
2. Create at least one endpoint
3. Regenerate tests (will auto-link)
4. Or manually configure each scenario

---

## **Best Practices**

### **1. Provide Good Example Values in Excel**

**Good:**
```
Field: fiscalYear
Example: "2025"
```

**Bad:**
```
Field: fiscalYear
Example: ""
```

AI uses example values to generate realistic test data.

### **2. Write Clear Validation Rules**

**Good:**
```
Validation Rule: Must be 4-digit year between 2020-2030
```

**Bad:**
```
Validation Rule: Valid year
```

Clear rules help AI generate better expected responses.

### **3. Review AI-Generated Scenarios**

- Click "Configure" to review
- Verify request bodies match your API
- Adjust expected responses if needed
- Add edge cases AI might miss

### **4. Combine AI + Manual**

- Let AI generate base scenarios (saves time)
- Add custom scenarios for edge cases
- Configure AI scenarios for specific needs
- Build comprehensive test suite

---

## **Summary**

### **How Test Scenarios Are Created**

1. **AI-Generated (Enhanced)** ✨
   - Upload Excel → Click "Generate Tests"
   - AI creates complete scenarios with request/response JSON
   - Immediately runnable
   - Based on field mappings and validation rules

2. **Manual Custom** 🎯
   - Click "+ Create Custom Scenario"
   - Fill in form manually
   - Full control over all details

3. **Configure Existing** ⚙️
   - Start with AI-generated
   - Click "Configure" to adjust
   - Best of both worlds

### **Answer to Your Question**

**Q: How should we give the input/output JSON to test?**

**A: You have 3 options:**

1. **Let AI do it (Recommended)** - Upload Excel, AI generates everything
2. **Manual entry** - Use "Create Custom Scenario" form
3. **Hybrid** - AI generates, you configure/adjust

**Q: Can the system generate scenarios based on data mapping and endpoint?**

**A: Yes!** The enhanced AI generation:
- ✅ Analyzes your data mappings (fields, types, rules)
- ✅ Links to your configured endpoint
- ✅ Generates complete request bodies
- ✅ Generates expected responses
- ✅ Creates ready-to-run scenarios

---

**Restart the application and try uploading an Excel file to see the enhanced AI generation in action!** 🚀
