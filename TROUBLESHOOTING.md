# Troubleshooting Guide

## File Upload Error

If you see "Error uploading file" when trying to upload an Excel file, follow these steps:

### 1. Check Backend Server is Running

The backend must be running on `http://localhost:8000`. To verify:

1. Open a browser and go to: `http://localhost:8000`
2. You should see: `{"message":"GS API Test Platform"}`
3. Check API docs at: `http://localhost:8000/docs`

### 2. Start Servers in Debug Mode

Use the debug startup script to see detailed error messages:

```bash
.\start-debug.bat
```

This will open two separate windows:
- **Backend window**: Shows FastAPI server logs and any Python errors
- **Frontend window**: Shows Vite dev server logs

**Check the backend window for errors like:**
- `ModuleNotFoundError` - Missing Python packages
- `PermissionError` - File/folder access issues
- `Database errors` - SQLite issues
- `Port already in use` - Another process using port 8000

### 3. Common Issues and Solutions

#### Backend Not Starting

**Problem**: Backend window shows `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies globally (since we're not using venv):
```bash
pip install fastapi uvicorn sqlalchemy pandas openpyxl openai python-multipart
```

#### Port Already in Use

**Problem**: `Address already in use` or `Port 8000 is already allocated`

**Solution**: Kill the existing process:
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

#### CORS Error

**Problem**: Browser console shows CORS error

**Solution**: Verify backend CORS settings allow `http://localhost:5173`
- Check `backend/main.py` line 18 has correct origin

#### Database Error

**Problem**: SQLite database errors

**Solution**: Delete and recreate the database:
```bash
cd backend
del gs_api_test.db
# Restart backend - it will recreate the database
```

#### Azure OpenAI Not Configured

**Problem**: File uploads but parsing fails

**Solution**: Configure Azure OpenAI credentials in `backend/.env`:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

### 4. Test Backend Manually

Test the upload endpoint directly:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test upload (replace with your Excel file path)
curl -X POST "http://localhost:8000/api/mappings/upload" -F "file=@C:\path\to\your\file.xlsx"
```

### 5. Check Browser Console

Open browser Developer Tools (F12) and check:
- **Console tab**: Look for JavaScript errors or failed fetch requests
- **Network tab**: Check the upload request status and response

### 6. Verify File Permissions

Ensure the backend can write to the uploads folder:
```bash
cd backend
mkdir uploads
# Verify you can create files in this folder
```

### 7. Frontend Issues

**Problem**: Frontend not loading

**Solution**: 
```bash
cd frontend
npm install
npm run dev
```

### 8. Complete Reset

If nothing works, do a complete reset:

```bash
# 1. Stop all servers (close all windows)

# 2. Clean backend
cd backend
del gs_api_test.db
rmdir /s /q uploads
mkdir uploads

# 3. Reinstall frontend dependencies
cd ..\frontend
rmdir /s /q node_modules
npm install

# 4. Start in debug mode
cd ..
.\start-debug.bat
```

## Getting Help

When reporting issues, include:
1. Error message from backend window
2. Error message from frontend window
3. Browser console errors (F12 → Console tab)
4. Network request details (F12 → Network tab)
5. Python version: `python --version`
6. Node version: `node --version`
