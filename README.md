# GS API Test Platform

A minimal test automation platform for GS API mappings with AI-powered field parsing and test generation.

## Architecture

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + Vite + Tailwind CSS
- **AI**: Azure OpenAI for parsing and test generation

## Features

1. **Upload Excel Mappings** - Upload Excel files containing API field mappings
2. **AI-Powered Parsing** - Automatically parse fields with Claude AI
3. **Field Approval** - Review and approve parsed fields
4. **Test Generation** - Generate test scenarios based on parsed fields
5. **Validation** - Run validation tests and view results

## Setup

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

5. Add your Azure OpenAI credentials to `.env`:
```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

6. Run the server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## Usage

1. **Upload**: Upload an Excel file with API field mappings
2. **Wait for Parsing**: AI will automatically parse the fields (check status)
3. **Review Fields**: View parsed fields in the "Parsed Fields" tab
4. **Generate Tests**: Click "Generate Tests" to create test scenarios
5. **Run Tests**: Go to "Test Scenarios" tab and run individual scenarios
6. **View Results**: Check validation results in the "Results" tab

## Database Schema

- **Mapping**: Uploaded files metadata
- **ParsedField**: AI-parsed field information with GS rules
- **TestScenario**: Generated test cases
- **ValidationResult**: Test execution results

## API Endpoints

- `POST /api/mappings/upload` - Upload Excel file
- `GET /api/mappings` - List all mappings
- `GET /api/mappings/{id}/fields` - Get parsed fields
- `PUT /api/fields/{id}/approve` - Approve a field
- `POST /api/mappings/{id}/generate-tests` - Generate test scenarios
- `GET /api/mappings/{id}/scenarios` - Get test scenarios
- `POST /api/scenarios/{id}/run` - Run validation
- `GET /api/scenarios/{id}/results` - Get validation results

## Tech Stack

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- SQLite - Database
- Pandas - Excel processing
- Azure OpenAI - AI integration
- Uvicorn - ASGI server

### Frontend
- React 18 - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Fetch API - HTTP client

## Future Enhancements

- PostgreSQL migration
- Celery for async tasks
- Vendor data integration
- DB reconciliation
- Advanced reporting
- Authentication
