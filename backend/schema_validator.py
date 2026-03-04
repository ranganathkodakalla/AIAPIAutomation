"""
Comprehensive Schema Validation Engine
Validates ONLY JSON structure and field presence (no type checking, no data validation)
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

class SchemaValidator:
    """Schema-only validation engine with 22 checks across 10 tiers"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.results = []
        
    def get_nested_value(self, obj: Any, path: str) -> Tuple[Any, Optional[str]]:
        """
        Navigate nested path in JSON object
        Returns: (value, error_message)
        """
        # Remove array markers and split path
        parts = path.replace('[]', '').split('.')
        current = obj
        
        for i, part in enumerate(parts):
            # If current is a list, get first item
            if isinstance(current, list):
                if len(current) > 0:
                    current = current[0]
                else:
                    return None, f"Empty array at level: {'.'.join(parts[:i])}"
            
            # Navigate into object
            if isinstance(current, dict):
                if part not in current:
                    return None, f"Missing at level: {'.'.join(parts[:i+1])}"
                current = current[part]
            else:
                return None, f"Not an object at level: {'.'.join(parts[:i])}"
        
        return current, None
    
    def detect_dataset(self, data: Any) -> Tuple[Optional[List], Optional[str]]:
        """
        Detect dataset array in response
        Returns: (dataset_array, dataset_key)
        """
        if isinstance(data, list):
            return data, '[root array]'
        
        if isinstance(data, dict):
            # Try common dataset keys
            for key in ['entityData', 'data', 'results', 'items', 'records', 'entries', 'termsAndConditions']:
                if key in data and isinstance(data[key], list):
                    return data[key], key
        
        return None, None
    
    def add_result(self, scenario_id: int, execution_id: int, field_name: str, 
                   validation_type: str, expected: str, actual: str, 
                   status: str, root_cause: str = None):
        """Add validation result to results list"""
        self.results.append({
            'scenario_id': scenario_id,
            'execution_id': execution_id,
            'field_name': field_name,
            'validation_type': validation_type,
            'expected': expected,
            'actual': actual,
            'status': status,
            'root_cause': root_cause,
            'timestamp': datetime.utcnow()
        })
    
    def validate_schema(self, scenario_id: int, execution_id: int, endpoint_url: str, 
                       method: str, headers: Dict, request_body: Any, 
                       parsed_fields: List, timeout: int = 30) -> Dict:
        """
        Execute comprehensive schema validation
        Returns: validation summary with all results
        """
        self.results = []
        
        # Make API call
        try:
            if method.upper() == 'GET':
                response = requests.get(endpoint_url, headers=headers, timeout=timeout)
            elif method.upper() == 'POST':
                response = requests.post(endpoint_url, json=request_body, headers=headers, timeout=timeout)
            elif method.upper() == 'PUT':
                response = requests.put(endpoint_url, json=request_body, headers=headers, timeout=timeout)
            elif method.upper() == 'PATCH':
                response = requests.patch(endpoint_url, json=request_body, headers=headers, timeout=timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(endpoint_url, headers=headers, timeout=timeout)
            else:
                self.add_result(scenario_id, execution_id, '_api_call', 'schema',
                              'valid HTTP method', f'unsupported: {method}', 'fail',
                              f'HTTP method {method} is not supported')
                return self._build_summary()
        
        except requests.RequestException as e:
            self.add_result(scenario_id, execution_id, '_api_call', 'schema',
                          'successful API call', f'failed: {str(e)}', 'fail',
                          f'Unable to reach API endpoint: {str(e)}')
            return self._build_summary()
        
        # === TIER 1: HTTP & RESPONSE BASICS ===
        
        # CHECK 1: HTTP Status Code
        status_code = response.status_code
        is_success = 200 <= status_code < 300
        is_client_error = 400 <= status_code < 500
        is_server_error = 500 <= status_code < 600
        
        status_category = '2xx' if is_success else '4xx' if is_client_error else '5xx' if is_server_error else 'other'
        
        self.add_result(scenario_id, execution_id, '_http_status', 'schema',
                       '2xx success', f'{status_code} ({status_category})',
                       'pass' if is_success else 'fail',
                       None if is_success else f'Expected success status (2xx), got {status_code}')
        
        # CHECK 2: Response Headers - Content-Type
        content_type = response.headers.get('Content-Type', '')
        is_json = 'application/json' in content_type
        
        self.add_result(scenario_id, execution_id, '_content_type', 'schema',
                       'application/json', content_type,
                       'pass' if is_json else 'fail',
                       None if is_json else 'Response Content-Type is not application/json')
        
        # CHECK 2b: Required Headers
        required_headers = ['Content-Type', 'Date']
        missing_headers = [h for h in required_headers if h not in response.headers]
        
        self.add_result(scenario_id, execution_id, '_required_headers', 'schema',
                       'all required headers present', 
                       'present' if not missing_headers else f'missing: {missing_headers}',
                       'pass' if not missing_headers else 'fail',
                       f'Missing required headers: {missing_headers}' if missing_headers else None)
        
        # CHECK 3: Response Size
        response_size = len(response.content)
        is_non_empty = response_size > 0 or status_code == 204
        
        self.add_result(scenario_id, execution_id, '_response_size', 'schema',
                       'non-empty response', f'{response_size} bytes',
                       'pass' if is_non_empty else 'fail',
                       'Response body is empty' if not is_non_empty else None)
        
        # === TIER 2: JSON STRUCTURE ===
        
        # CHECK 4: JSON Parseable
        try:
            data = response.json()
            self.add_result(scenario_id, execution_id, '_json_valid', 'schema',
                           'Valid JSON', 'Valid', 'pass')
        except json.JSONDecodeError as e:
            self.add_result(scenario_id, execution_id, '_json_valid', 'schema',
                           'Valid JSON', f'Parse error: {str(e)}', 'fail',
                           'Response is not valid JSON. Check API response format.')
            return self._build_summary()
        
        # CHECK 5: Root Structure
        root_type = 'array' if isinstance(data, list) else 'object' if isinstance(data, dict) else 'unknown'
        
        self.add_result(scenario_id, execution_id, '_root_type', 'schema',
                       'object or array', root_type,
                       'pass' if root_type in ['object', 'array'] else 'fail',
                       f'Root is {root_type}, expected object or array' if root_type not in ['object', 'array'] else None)
        
        # === TIER 3: DATASET PRESENCE ===
        
        # CHECK 6: Dataset Detection
        dataset, dataset_key = self.detect_dataset(data)
        
        self.add_result(scenario_id, execution_id, '_dataset_found', 'schema',
                       'dataset present', f'Found: {dataset_key}' if dataset_key else 'No dataset found',
                       'pass' if dataset else 'warning',
                       'No dataset array found in response' if not dataset else None)
        
        # CHECK 7: Dataset Non-Empty
        if dataset is not None:
            dataset_count = len(dataset)
            self.add_result(scenario_id, execution_id, '_dataset_count', 'schema',
                           '> 0 records', f'{dataset_count} records',
                           'pass' if dataset_count > 0 else 'warning',
                           'Dataset is empty' if dataset_count == 0 else None)
        
        # CHECK 8: Pagination Metadata
        if isinstance(data, dict):
            pagination_fields = ['totalRecords', 'page', 'size', 'totalPages', 'limit', 'offset']
            found_pagination = [f for f in pagination_fields if f in data]
            
            link_fields = ['links', 'selfLink', 'nextLink', 'prevLink', 'firstLink', 'lastLink']
            found_links = [f for f in link_fields if f in data]
            
            has_pagination = len(found_pagination) > 0 or len(found_links) > 0
            
            pagination_info = ', '.join(found_pagination + found_links) if has_pagination else 'No pagination'
            
            self.add_result(scenario_id, execution_id, '_pagination', 'schema',
                           'pagination metadata', pagination_info, 'info')
        
        # === TIER 4 & 5: REQUIRED FIELDS PRESENCE & PATH NAVIGATION ===
        
        # Get first record for nested field checks
        first_record = dataset[0] if dataset and len(dataset) > 0 else {}
        
        # Track which fields we've checked
        checked_fields = set()
        
        for field in parsed_fields:
            field_path = field.field_name
            
            # Skip if already checked
            if field_path in checked_fields:
                continue
            checked_fields.add(field_path)
            
            # Determine where to look for this field
            if any(prefix in field_path for prefix in ['entityData[]', 'data[]', 'results[]', 'items[]', 'records[]', 'termsAndConditions[]']):
                # Record-level field - check in first record
                check_obj = first_record
            else:
                # Top-level field - check in root data
                check_obj = data
            
            # CHECK 9/10: Field Presence
            value, error = self.get_nested_value(check_obj, field_path)
            
            if error:
                # Field is missing
                status = 'fail' if field.required else 'info'
                self.add_result(scenario_id, execution_id, field_path, 'schema',
                               'field present' if field.required else 'optional field',
                               'missing', status,
                               f"{'Required' if field.required else 'Optional'} field '{field_path}' not found. {error}")
            
            elif value is None:
                # CHECK 19: Null vs Missing
                status = 'fail' if field.required else 'info'
                self.add_result(scenario_id, execution_id, field_path, 'schema',
                               'non-null value' if field.required else 'optional field',
                               'null', status,
                               f"Field '{field_path}' is null" if field.required else None)
            
            else:
                # Field is present
                self.add_result(scenario_id, execution_id, field_path, 'schema',
                               'field present', 'present', 'pass')
                
                # CHECK 12: Array Structure Check
                if '[]' in field_path and isinstance(value, list):
                    self.add_result(scenario_id, execution_id, f'{field_path}._type', 'schema',
                                   'array type', 'array', 'pass')
                    
                    # CHECK 20: Null in Arrays
                    if None in value:
                        self.add_result(scenario_id, execution_id, f'{field_path}._null_items', 'schema',
                                       'no null items', 'contains null', 'warning',
                                       f'Array {field_path} contains null items')
                
                elif '[]' in field_path and not isinstance(value, list):
                    self.add_result(scenario_id, execution_id, f'{field_path}._type', 'schema',
                                   'array type', type(value).__name__, 'fail',
                                   f'Expected array but got {type(value).__name__}')
        
        # === TIER 6: OPTIONAL FIELDS DISCOVERY ===
        
        # CHECK 14: Optional Fields
        optional_fields = [f for f in parsed_fields if not f.required]
        for field in optional_fields:
            if field.field_name not in checked_fields:
                field_path = field.field_name
                check_obj = first_record if any(p in field_path for p in ['entityData[]', 'data[]', 'results[]']) else data
                value, error = self.get_nested_value(check_obj, field_path)
                
                if not error and value is not None:
                    self.add_result(scenario_id, execution_id, field_path, 'schema',
                                   'optional field', 'found', 'info')
        
        # === TIER 7: UNEXPECTED FIELDS DETECTION ===
        
        # CHECK 15: Extra Fields
        mapped_field_names = set(f.field_name.split('.')[0].replace('[]', '') for f in parsed_fields)
        
        if isinstance(data, dict):
            actual_fields = set(data.keys())
            extra_fields = actual_fields - mapped_field_names
            
            if extra_fields:
                self.add_result(scenario_id, execution_id, '_extra_fields', 'schema',
                               'no unexpected fields', f'found: {list(extra_fields)}', 'warning',
                               f'Response contains unmapped fields: {list(extra_fields)}')
        
        # CHECK 16: Deprecated Fields
        if isinstance(data, dict):
            actual_fields = set(data.keys())
            top_level_mapped = set(f.field_name.split('.')[0].replace('[]', '') for f in parsed_fields if '.' not in f.field_name or f.field_name.startswith('entityData'))
            missing_mapped = top_level_mapped - actual_fields - {'entityData', 'data', 'results', 'items', 'records'}
            
            if missing_mapped:
                self.add_result(scenario_id, execution_id, '_missing_mapped_fields', 'schema',
                               'all mapped fields present', f'missing: {list(missing_mapped)}', 'warning',
                               f'Mapped fields not in response: {list(missing_mapped)}')
        
        # === TIER 8: ERROR RESPONSE HANDLING ===
        
        # CHECK 17 & 18: Error Response Structure (for 4xx/5xx)
        if is_client_error or is_server_error:
            error_fields = ['error', 'message', 'code', 'details', 'status']
            found_error_fields = [f for f in error_fields if f in data] if isinstance(data, dict) else []
            
            has_error_structure = len(found_error_fields) > 0
            
            self.add_result(scenario_id, execution_id, '_error_structure', 'schema',
                           'error object present', 'present' if has_error_structure else 'missing',
                           'pass' if has_error_structure else 'fail',
                           'Error response missing standard error fields' if not has_error_structure else None)
            
            if has_error_structure and isinstance(data, dict):
                # Check error message is non-empty
                error_msg = data.get('error') or data.get('message')
                if error_msg and isinstance(error_msg, str) and len(error_msg) > 0:
                    self.add_result(scenario_id, execution_id, 'error.message', 'schema',
                                   'non-empty error message', 'present', 'pass')
                else:
                    self.add_result(scenario_id, execution_id, 'error.message', 'schema',
                                   'non-empty error message', 'missing or empty', 'fail',
                                   'Error response has no message')
        
        # === TIER 10: CONSISTENCY CHECKS ===
        
        # CHECK 21: Multi-Record Consistency
        if dataset and len(dataset) > 1:
            sample_size = min(5, len(dataset))
            inconsistent_fields = []
            
            # Get required fields that should be in all records
            required_record_fields = [f.field_name for f in parsed_fields 
                                     if f.required and any(p in f.field_name for p in ['entityData[]', 'data[]', 'results[]', 'termsAndConditions[]'])]
            
            for field_path in required_record_fields:
                for i in range(sample_size):
                    value, error = self.get_nested_value(dataset[i], field_path)
                    if error or value is None:
                        inconsistent_fields.append(f"{field_path} missing in record {i}")
                        break
            
            self.add_result(scenario_id, execution_id, '_schema_consistency', 'schema',
                           'consistent schema across records',
                           'consistent' if not inconsistent_fields else f'inconsistent: {inconsistent_fields[:3]}',
                           'pass' if not inconsistent_fields else 'fail',
                           f'Schema varies across records: {inconsistent_fields}' if inconsistent_fields else None)
        
        return self._build_summary()
    
    def _build_summary(self) -> Dict:
        """Build validation summary from results"""
        total_checks = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'pass')
        failed = sum(1 for r in self.results if r['status'] == 'fail')
        warnings = sum(1 for r in self.results if r['status'] == 'warning')
        info = sum(1 for r in self.results if r['status'] == 'info')
        
        return {
            'validation_type': 'schema_only',
            'total_checks': total_checks,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'info': info,
            'results': self.results
        }
