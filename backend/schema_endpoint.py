"""
Schema validation API endpoint
Separate file for cleaner organization
"""
from fastapi import HTTPException
from schema_validator import SchemaValidator
from datetime import datetime
import json

def execute_schema_validation_endpoint(scenario_id: int, db):
    """
    Execute schema-only validation for a scenario
    POST /api/scenarios/{scenario_id}/execute-schema
    """
    from main import TestScenario, APIEndpoint, ParsedField, TestExecution, ValidationResult, get_or_fetch_token
    
    # Fetch scenario
    scenario = db.query(TestScenario).filter(TestScenario.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Fetch endpoint
    if not scenario.endpoint_id:
        raise HTTPException(status_code=400, detail="Scenario has no endpoint configured")
    
    endpoint = db.query(APIEndpoint).filter(APIEndpoint.id == scenario.endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    # Fetch parsed fields for validation
    if not scenario.mapping_id:
        raise HTTPException(status_code=400, detail="Scenario has no mapping configured")
    
    parsed_fields = db.query(ParsedField).filter(ParsedField.mapping_id == scenario.mapping_id).all()
    
    # Create execution record
    execution = TestExecution(
        scenario_id=scenario_id,
        status="running",
        execution_date=datetime.utcnow()
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    try:
        # Prepare request
        url = f"{endpoint.base_url}{endpoint.path}"
        headers = {}
        
        if endpoint.headers:
            headers = json.loads(endpoint.headers)
        
        # Handle token dependency
        if endpoint.token_endpoint_id:
            token = get_or_fetch_token(endpoint.id, db)
            if token:
                headers["Authorization"] = f"Bearer {token}"
        elif endpoint.auth_type == "bearer" and endpoint.auth_token:
            headers["Authorization"] = f"Bearer {endpoint.auth_token}"
        elif endpoint.auth_type == "api_key" and endpoint.auth_token:
            headers["X-API-Key"] = endpoint.auth_token
        
        # Prepare request body
        request_body = None
        if scenario.request_body:
            try:
                request_body = json.loads(scenario.request_body)
            except:
                request_body = {}
        
        # Execute schema validation
        validator = SchemaValidator(db)
        summary = validator.validate_schema(
            scenario_id=scenario_id,
            execution_id=execution.id,
            endpoint_url=url,
            method=endpoint.method,
            headers=headers,
            request_body=request_body,
            parsed_fields=parsed_fields,
            timeout=endpoint.timeout_ms // 1000
        )
        
        # Save validation results to database
        for result_data in summary['results']:
            result = ValidationResult(
                scenario_id=result_data['scenario_id'],
                execution_id=result_data['execution_id'],
                field_name=result_data['field_name'],
                expected=result_data['expected'],
                actual=result_data['actual'],
                status=result_data['status'],
                root_cause=result_data.get('root_cause'),
                validation_type=result_data['validation_type'],
                timestamp=result_data['timestamp']
            )
            db.add(result)
        
        # Update execution record
        execution.status = "completed"
        execution.pass_count = summary['passed']
        execution.fail_count = summary['failed']
        db.commit()
        
        # Add execution_id to summary
        summary['execution_id'] = execution.id
        summary['scenario_id'] = scenario_id
        
        return summary
        
    except Exception as e:
        execution.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Schema validation failed: {str(e)}")
