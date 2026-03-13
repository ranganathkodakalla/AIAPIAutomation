# Certificate-Based Authentication Guide

## Overview
The API Testing Platform now supports **Client Certificate Authentication with Password** for endpoints that require certificate-based security (e.g., .pfx or .p12 certificates).

## Configuration Steps

### 1. Create/Edit Endpoint with Certificate Auth

1. Go to **Endpoints** tab
2. Click **"New Endpoint"** or edit an existing endpoint
3. Fill in basic details (Name, Method, Base URL, Path)
4. In **Auth Type** dropdown, select: **"Client Certificate (with Password)"**
5. Two new fields will appear:
   - **Certificate Path**: Full path to your certificate file
     - Example: `C:\certs\mycert.pfx` or `/etc/ssl/certs/mycert.p12`
   - **Certificate Password**: Password to unlock the certificate

### 2. Certificate File Formats Supported
- `.pfx` (PKCS#12 format) - Windows
- `.p12` (PKCS#12 format) - Cross-platform

### 3. Example Configuration

```
Name: Secure API Endpoint
Method: POST
Base URL: https://secure-api.example.com
Path: /api/v1/data
Auth Type: Client Certificate (with Password)
Certificate Path: C:\certificates\client-cert.pfx
Certificate Password: ********
```

## Database Schema

The following columns were added to the `api_endpoints` table:
- `cert_path` (TEXT) - Stores the certificate file path
- `cert_password` (TEXT) - Stores the certificate password (encrypted in production)

## Security Considerations

⚠️ **Important Security Notes:**

1. **Certificate Storage**: Store certificates in a secure location with restricted access
2. **Password Security**: Certificate passwords are stored in the database - consider encryption for production
3. **File Permissions**: Ensure certificate files have appropriate read permissions
4. **Path Validation**: Always use absolute paths to certificate files

## Testing Certificate Authentication

1. Configure endpoint with certificate details
2. Click **"Test Connection"** button
3. The system will:
   - Load the certificate from the specified path
   - Use the password to unlock it
   - Make a test request with the certificate attached
   - Display connection results

## Troubleshooting

### Common Issues:

**Certificate Not Found**
- Verify the certificate path is correct and absolute
- Check file permissions
- Ensure the file exists at the specified location

**Invalid Password**
- Verify the certificate password is correct
- Check for special characters or encoding issues

**Certificate Format Error**
- Ensure the certificate is in .pfx or .p12 format
- Try converting the certificate to PKCS#12 format

## Migration

The database migration was completed automatically. If you need to run it manually:

```bash
cd backend
python add_certificate_columns.py
```

## API Response

Endpoints with certificate authentication will return:
```json
{
  "id": 1,
  "name": "Secure Endpoint",
  "auth_type": "certificate",
  "cert_path": "C:\\certs\\mycert.pfx",
  "cert_password": "****",
  ...
}
```

## Next Steps

After configuration:
1. Test the endpoint connection
2. Create test scenarios
3. Run automated tests
4. Monitor results in the dashboard

---

**Last Updated**: March 13, 2026
**Feature Version**: 1.0
