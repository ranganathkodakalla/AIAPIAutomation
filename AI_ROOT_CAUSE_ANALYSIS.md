# AI-Powered Root Cause Analysis System

## Overview
This system analyzes every validation failure and provides plain-English diagnosis in seconds using Azure OpenAI.

## Features Implemented

### 1. Database Schema ✅
- **ValidationResult Model**: Added `root_cause_category`, `suggested_action`, `ai_confidence` fields
- **RootCauseCache Model**: Caches AI analyses to avoid redundant API calls
- **Migration Script**: `migrate_add_ai_root_cause.py`

### 2. Root Cause Categories
Seven standard categories for classification:
- **API_BUG**: API is returning incorrect data
- **DATA_TRANSFORMATION**: Mapping/conversion issue between systems
- **VENDOR_DATA**: Test data was not created correctly
- **STALE_CACHE**: API returning cached/outdated data
- **BUSINESS_RULE**: Field violates a conditional rule
- **MISSING_SYNC**: Related fields are out of sync
- **CONFIGURATION**: API endpoint or parameters incorrect

### 3. Backend Endpoints ✅

#### POST /api/failures/{validation_result_id}/analyze
Analyze a single validation failure with comprehensive context:
- Gathers field metadata from Excel mapping
- Collects related field values from same API response
- Analyzes historical patterns (last 10 runs)
- Caches results for performance
- Returns detailed root cause analysis

**Response:**
```json
{
  "root_cause_category": "BUSINESS_RULE",
  "explanation": "Status is INACTIVE but balance is non-zero (500.00)...",
  "suggested_action": "Check the database stored procedure...",
  "confidence": 87,
  "from_cache": false
}
```

#### POST /api/scenarios/{scenario_id}/analyze-all-failures
Batch analyze all failures from a scenario execution:
- Processes all failed validations
- Uses cached analyses when available
- Rate-limited to avoid API throttling
- Returns comprehensive analysis for each failure

**Response:**
```json
{
  "total_failures": 15,
  "analyses": [
    {
      "validation_result_id": 123,
      "field": "status",
      "root_cause": "...",
      "category": "BUSINESS_RULE",
      "suggested_action": "...",
      "confidence": 87,
      "cached": false
    }
  ]
}
```

#### GET /api/scenarios/{scenario_id}/insights
Generate AI-powered insights by analyzing patterns:
- Groups failures by category
- Identifies patterns across multiple failures
- Prioritizes by severity (critical/warning/info)
- Provides actionable next steps

**Response:**
```json
{
  "insights": [
    {
      "severity": "critical",
      "title": "60% of failures in address fields",
      "description": "Vendor data incomplete for address validation",
      "affected_fields": 9,
      "suggested_action": "Contact vendor to complete test data"
    }
  ],
  "total_failures": 15,
  "categories": {
    "VENDOR_DATA": 9,
    "BUSINESS_RULE": 4,
    "API_BUG": 2
  }
}
```

### 4. AI Analysis Process

**Context Gathering:**
1. Failed field details (name, type, expected, actual)
2. Parsed field metadata (data type, required, validation rule)
3. Related field values (up to 10 from same response)
4. Historical patterns (pass rate, common failures)
5. Field path context (nested, array position)

**Caching Strategy:**
- Cache key: `{field_name}:{expected}:{actual}`
- Stores: category, explanation, suggested_action, confidence
- Automatic cache lookup before AI call
- Significant performance improvement for repeated failures

**AI Prompt Structure:**
- Comprehensive failure context
- Field metadata and validation rules
- Related field values
- Historical patterns
- Specific analysis instructions
- Structured JSON response format

### 5. Performance Optimizations ✅
- **Caching**: Avoids redundant AI calls for identical failures
- **Batch Processing**: Analyzes multiple failures with rate limiting
- **Context Limiting**: Max 10 related fields, truncated values
- **Historical Window**: Last 10 runs only

## Frontend Integration (To Be Implemented)

### Expandable Root Cause Panels
When user clicks a FAILED row:
- Display AI root cause category with icon
- Show 2-3 sentence explanation
- Provide specific suggested action
- Display confidence score
- Show related field values

### AI Insights Panel
Proactive insights at top of Scenario tab:
- Top 3-5 actionable insights
- Severity indicators (critical/warning/info)
- Pattern detection across failures
- Affected field counts
- Specific next steps

## Migration Instructions

1. **Run Migration:**
   ```bash
   cd backend
   python migrate_add_ai_root_cause.py
   ```

2. **Restart Backend:**
   ```bash
   cd ..
   .\start.bat
   ```

3. **Test Endpoints:**
   - Run a scenario with failures
   - Call `/api/scenarios/{scenario_id}/analyze-all-failures`
   - View AI analysis results

## Usage Examples

### Analyze Single Failure
```bash
curl -X POST http://localhost:8000/api/failures/123/analyze
```

### Analyze All Failures in Scenario
```bash
curl -X POST http://localhost:8000/api/scenarios/5/analyze-all-failures
```

### Get AI Insights
```bash
curl http://localhost:8000/api/scenarios/5/insights
```

## Configuration

Requires Azure OpenAI credentials in `.env`:
```
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

## Next Steps

1. **Frontend UI**: Implement expandable panels and insights display
2. **Testing**: Validate with real failure scenarios
3. **Refinement**: Tune AI prompts based on results
4. **Documentation**: Add user guide for interpreting analyses

## Benefits

- **Speed**: Instant diagnosis in seconds vs manual analysis
- **Accuracy**: Context-aware analysis with 70-90% confidence
- **Actionable**: Specific next steps, not generic advice
- **Learning**: Caches analyses for performance
- **Patterns**: Identifies systemic issues across failures
