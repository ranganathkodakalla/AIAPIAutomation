# 🔍 Schema-Only Validation Engine - Complete Guide

## **Overview**

The Schema-Only Validation Engine validates **ONLY JSON structure and field presence** - no type checking, no data validation. This is perfect for:

- ✅ Verifying API response structure
- ✅ Checking required fields are present
- ✅ Detecting breaking changes (missing/extra fields)
- ✅ Validating pagination metadata
- ✅ Ensuring consistent schema across records
- ✅ Testing error response formats

---

## **22 Validation Checks Across 10 Tiers**

### **TIER 1: HTTP & Response Basics**

#### **Check 1: HTTP Status Code**
- **Purpose:** Verify API returns correct status code
- **Expected:** 2xx for success, 4xx for client errors, 5xx for server errors
- **Example:**
  ```
  Expected: 2xx success
  Actual: 200 (2xx)
  Status: PASS ✅
  ```

#### **Check 2: Response Headers - Content-Type**
- **Purpose:** Ensure response is JSON
- **Expected:** `application/json`
- **Example:**
  ```
  Expected: application/json
  Actual: application/json; charset=utf-8
  Status: PASS ✅
  ```

#### **Check 2b: Required Headers**
- **Purpose:** Verify essential headers are present
- **Expected:** Content-Type, Date
- **Example:**
  ```
  Expected: all required headers present
  Actual: present
  Status: PASS ✅
  ```

#### **Check 3: Response Size**
- **Purpose:** Ensure response is not empty
- **Expected:** Non-empty response (unless 204 No Content)
- **Example:**
  ```
  Expected: non-empty response
  Actual: 6130 bytes
  Status: PASS ✅
  ```

---

### **TIER 2: JSON Structure**

#### **Check 4: JSON Parseable**
- **Purpose:** Verify response is valid JSON
- **Expected:** Valid JSON
- **Example:**
  ```
  Expected: Valid JSON
  Actual: Valid
  Status: PASS ✅
  ```
  
  **Failure Example:**
  ```
  Expected: Valid JSON
  Actual: Parse error: Expecting value: line 1 column 1 (char 0)
  Status: FAIL ❌
  Root Cause: Response is not valid JSON. Check API response format.
  ```

#### **Check 5: Root Structure**
- **Purpose:** Identify if response is object or array
- **Expected:** object or array
- **Example:**
  ```
  Expected: object or array
  Actual: object
  Status: PASS ✅
  ```

---

### **TIER 3: Dataset Presence**

#### **Check 6: Dataset Detection**
- **Purpose:** Find the main data array in response
- **Expected:** dataset present
- **Looks for:** entityData, data, results, items, records, entries, termsAndConditions
- **Example:**
  ```
  Expected: dataset present
  Actual: Found: termsAndConditions
  Status: PASS ✅
  ```

#### **Check 7: Dataset Non-Empty**
- **Purpose:** Verify dataset contains records
- **Expected:** > 0 records
- **Example:**
  ```
  Expected: > 0 records
  Actual: 6 records
  Status: PASS ✅
  ```

#### **Check 8: Pagination Metadata**
- **Purpose:** Detect pagination fields
- **Expected:** pagination metadata
- **Looks for:** totalRecords, page, size, totalPages, limit, offset, links, selfLink, nextLink
- **Example:**
  ```
  Expected: pagination metadata
  Actual: totalRecords, limit, currentBatchSize, links
  Status: INFO ℹ️
  ```

---

### **TIER 4: Required Fields Presence**

#### **Check 9: Top-Level Required Fields**
- **Purpose:** Verify required fields exist at root level
- **Example:**
  ```
  Field: totalRecords
  Expected: field present
  Actual: present
  Status: PASS ✅
  ```

#### **Check 10: Record-Level Required Fields**
- **Purpose:** Verify required fields exist in dataset records
- **Example:**
  ```
  Field: termsAndConditions[].title
  Expected: field present
  Actual: present
  Status: PASS ✅
  ```

---

### **TIER 5: Field Path Navigation**

#### **Check 11: Nested Object Navigation**
- **Purpose:** Verify nested paths are navigable
- **Example:**
  ```
  Field: coreData.physicalAddress.city
  Expected: navigable path
  Actual: success
  Status: PASS ✅
  ```
  
  **Failure Example:**
  ```
  Field: coreData.physicalAddress.city
  Expected: navigable path
  Actual: broken at coreData.physicalAddress
  Status: FAIL ❌
  Root Cause: Not an object at level: coreData
  ```

#### **Check 12: Array Structure**
- **Purpose:** Verify fields marked as arrays are actually arrays
- **Example:**
  ```
  Field: termsAndConditions[]._type
  Expected: array type
  Actual: array
  Status: PASS ✅
  ```

#### **Check 13: Array Item Schema**
- **Purpose:** Verify array items have consistent structure
- **Example:**
  ```
  Field: naicsList[0].naicsCode
  Expected: present in items
  Actual: present
  Status: PASS ✅
  ```

---

### **TIER 6: Optional Fields Discovery**

#### **Check 14: Optional Fields**
- **Purpose:** Track which optional fields are present
- **Example:**
  ```
  Field: description (optional)
  Expected: optional field
  Actual: found
  Status: INFO ℹ️
  ```

---

### **TIER 7: Unexpected Fields Detection**

#### **Check 15: Extra Fields**
- **Purpose:** Detect fields in response not in mapping
- **Example:**
  ```
  Field: _extra_fields
  Expected: no unexpected fields
  Actual: found: ['newField', 'deprecatedField']
  Status: WARNING ⚠️
  Root Cause: Response contains unmapped fields: ['newField', 'deprecatedField']
  ```

#### **Check 16: Deprecated Fields**
- **Purpose:** Detect mapped fields missing from response
- **Example:**
  ```
  Field: _missing_mapped_fields
  Expected: all mapped fields present
  Actual: missing: ['oldField']
  Status: WARNING ⚠️
  Root Cause: Mapped fields not in response: ['oldField']
  ```

---

### **TIER 8: Error Response Handling**

#### **Check 17: Error Response Structure (4xx/5xx)**
- **Purpose:** Verify error responses have standard format
- **Expected:** error object present
- **Looks for:** error, message, code, details, status
- **Example:**
  ```
  Field: _error_structure
  Expected: error object present
  Actual: present
  Status: PASS ✅
  ```

#### **Check 18: Error Field Validation**
- **Purpose:** Verify error message is non-empty
- **Example:**
  ```
  Field: error.message
  Expected: non-empty error message
  Actual: present
  Status: PASS ✅
  ```

---

### **TIER 9: Null Handling**

#### **Check 19: Null vs Missing Distinction**
- **Purpose:** Distinguish between missing and null fields
- **For required fields:**
  - Missing entirely = FAIL
  - Present but null = FAIL
- **For optional fields:**
  - Missing = OK
  - Present but null = OK
- **Example:**
  ```
  Field: title
  Expected: non-null value
  Actual: null
  Status: FAIL ❌
  Root Cause: Field 'title' is null
  ```

#### **Check 20: Null in Arrays**
- **Purpose:** Detect null items in arrays
- **Example:**
  ```
  Field: naicsList[]._null_items
  Expected: no null items
  Actual: contains null
  Status: WARNING ⚠️
  Root Cause: Array naicsList[] contains null items
  ```

---

### **TIER 10: Consistency Checks**

#### **Check 21: Multi-Record Consistency**
- **Purpose:** Verify schema is consistent across all records
- **Samples:** First 5 records
- **Example:**
  ```
  Field: _schema_consistency
  Expected: consistent schema across records
  Actual: consistent
  Status: PASS ✅
  ```
  
  **Failure Example:**
  ```
  Field: _schema_consistency
  Expected: consistent schema across records
  Actual: inconsistent: ['title missing in record 2', 'grantProgramCode missing in record 4']
  Status: FAIL ❌
  Root Cause: Schema varies across records
  ```

#### **Check 22: Related Fields Presence**
- **Purpose:** Verify related fields appear together
- **Business Logic Examples:**
  - If zipCode present → city should be present
  - If naicsList[] present → primaryNaics should be present
- **Example:**
  ```
  Field: _related_fields
  Expected: X implies Y
  Actual: both present
  Status: PASS ✅
  ```

---

## **API Usage**

### **Endpoint**
```
POST /api/scenarios/{scenario_id}/execute-schema
```

### **Request**
```bash
curl -X POST http://localhost:8000/api/scenarios/1/execute-schema
```

### **Response Format**
```json
{
  "scenario_id": 1,
  "execution_id": 456,
  "validation_type": "schema_only",
  "total_checks": 45,
  "passed": 42,
  "failed": 2,
  "warnings": 1,
  "info": 3,
  "results": [
    {
      "scenario_id": 1,
      "execution_id": 456,
      "field_name": "_http_status",
      "validation_type": "schema",
      "expected": "2xx success",
      "actual": "200 (2xx)",
      "status": "pass",
      "root_cause": null,
      "timestamp": "2026-02-24T12:00:00Z"
    },
    {
      "scenario_id": 1,
      "execution_id": 456,
      "field_name": "title",
      "validation_type": "schema",
      "expected": "field present",
      "actual": "missing",
      "status": "fail",
      "root_cause": "Required field 'title' not found in response. Missing at level: title",
      "timestamp": "2026-02-24T12:00:00Z"
    }
  ]
}
```

---

## **Frontend Integration**

### **Run Schema Validation**
Add a new button next to the existing "Run" button:

```jsx
<button
  onClick={() => runSchemaValidation(scenario.id)}
  className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
>
  Schema Check
</button>
```

### **Display Results**
Results table with color coding:

| Field | Type | Expected | Actual | Status |
|-------|------|----------|--------|--------|
| _http_status | schema | 2xx success | 200 (2xx) | ✅ PASS |
| _content_type | schema | application/json | application/json | ✅ PASS |
| _json_valid | schema | Valid JSON | Valid | ✅ PASS |
| _dataset_found | schema | dataset present | Found: termsAndConditions | ✅ PASS |
| _dataset_count | schema | > 0 records | 6 records | ✅ PASS |
| title | schema | field present | present | ✅ PASS |
| grantProgramCode | schema | field present | missing | ❌ FAIL |
| _extra_fields | schema | no unexpected fields | found: ['newField'] | ⚠️ WARNING |
| description | schema | optional field | found | ℹ️ INFO |

### **Color Coding**
```css
.status-pass { color: #10b981; } /* Green */
.status-fail { color: #ef4444; } /* Red */
.status-warning { color: #f59e0b; } /* Orange */
.status-info { color: #3b82f6; } /* Blue */
```

---

## **Use Cases**

### **Use Case 1: API Contract Validation**
**Scenario:** Verify API response matches documented contract

**Schema Checks:**
- ✅ All required fields present
- ✅ No unexpected fields (breaking changes)
- ✅ Correct response structure (object/array)
- ✅ Pagination metadata present

**Result:** Contract compliance verified

---

### **Use Case 2: Breaking Change Detection**
**Scenario:** API updated, need to detect changes

**Schema Checks:**
- ⚠️ Extra fields detected: ['newFeatureFlag', 'betaEndpoint']
- ⚠️ Missing mapped fields: ['deprecatedField']
- ✅ All required fields still present

**Result:** Non-breaking changes detected, mapping needs update

---

### **Use Case 3: Error Response Validation**
**Scenario:** Test 404 error response format

**Schema Checks:**
- ✅ HTTP status: 404 (4xx)
- ✅ Error structure present
- ✅ Error message non-empty
- ✅ Error code present

**Result:** Error response follows standard format

---

### **Use Case 4: Multi-Record Consistency**
**Scenario:** Verify all records have same schema

**Schema Checks:**
- ✅ Schema consistent across 5 sampled records
- ✅ All required fields present in all records
- ✅ No null values in required fields

**Result:** Dataset has consistent structure

---

## **Comparison: Schema vs Full Validation**

| Feature | Schema Validation | Full Validation |
|---------|-------------------|-----------------|
| **HTTP Status** | ✅ Check | ✅ Check |
| **JSON Structure** | ✅ Check | ✅ Check |
| **Field Presence** | ✅ Check | ✅ Check |
| **Field Types** | ❌ Skip | ✅ Check (string/number/boolean) |
| **Data Validation** | ❌ Skip | ✅ Check (format, range, regex) |
| **Null Handling** | ✅ Check | ✅ Check |
| **Extra Fields** | ✅ Detect | ❌ Ignore |
| **Consistency** | ✅ Check | ❌ Skip |
| **Speed** | ⚡ Fast | 🐢 Slower |
| **Use Case** | Contract validation | Data quality testing |

---

## **Benefits**

### **1. Fast Execution**
- No type checking = faster validation
- Perfect for CI/CD pipelines
- Quick smoke tests

### **2. Breaking Change Detection**
- Detects new fields (API additions)
- Detects missing fields (API removals)
- Alerts on schema changes

### **3. Contract Compliance**
- Verifies API follows documented structure
- Ensures required fields always present
- Validates error response formats

### **4. Multi-Record Validation**
- Checks schema consistency across records
- Detects data quality issues
- Samples large datasets efficiently

---

## **Best Practices**

### **1. Use Schema Validation For:**
- ✅ Initial API testing (smoke tests)
- ✅ Contract validation
- ✅ Breaking change detection
- ✅ CI/CD pipeline checks
- ✅ Error response testing

### **2. Use Full Validation For:**
- ✅ Data quality testing
- ✅ Type validation
- ✅ Business logic validation
- ✅ Detailed field-level checks

### **3. Combine Both:**
```
1. Run schema validation first (fast)
2. If schema passes, run full validation (thorough)
3. If schema fails, fix structure before data validation
```

---

## **Troubleshooting**

### **Problem: "No dataset found"**
**Cause:** Response doesn't have common dataset keys

**Solution:**
- Check response structure
- Add custom dataset key to `detect_dataset()` function
- Verify API returns array of records

---

### **Problem: "Schema inconsistent across records"**
**Cause:** Different records have different fields

**Solution:**
- Check if API returns mixed record types
- Verify all records follow same schema
- Update mapping to include optional fields

---

### **Problem: "Extra fields detected"**
**Cause:** API added new fields not in mapping

**Solution:**
- Review new fields
- Update Excel mapping if needed
- Mark as optional if not critical

---

## **Summary**

The Schema-Only Validation Engine provides **22 comprehensive checks** across **10 tiers** to validate JSON structure and field presence without type checking. Perfect for:

- 🚀 Fast API contract validation
- 🔍 Breaking change detection
- ✅ Error response testing
- 📊 Multi-record consistency checks

**Use it to ensure your API responses have the correct structure before diving into detailed data validation!** 🎯
