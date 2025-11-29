# Swagger UI Documentation Guide

## Overview
Swagger UI has been successfully integrated into the Prudential Regulatory Backend System (PRBS) to provide interactive API documentation.

## Accessing the Documentation

Once your Django development server is running, you can access the API documentation at the following URLs:

### 1. Swagger UI (Interactive)
```
http://localhost:8000/swagger/
```
- **Interactive interface** to test API endpoints
- **Try it out** functionality for each endpoint
- **Request/Response examples**
- **Authentication support** (JWT Bearer tokens)

### 2. ReDoc (Alternative Documentation)
```
http://localhost:8000/redoc/
```
- **Clean, responsive** documentation interface
- **Better for reading** and understanding the API
- **Three-panel design** with navigation

### 3. OpenAPI Schema (JSON/YAML)
```
http://localhost:8000/swagger.json/
http://localhost:8000/swagger.yaml/
```
- **Raw schema files** for programmatic access
- **Can be imported** into other tools (Postman, Insomnia, etc.)

## Using Swagger UI with Authentication

Most endpoints in the PRBS API require JWT authentication. Here's how to authenticate:

### Step 1: Obtain a JWT Token
1. Navigate to the `/api/auth/login/` endpoint in Swagger UI
2. Click **"Try it out"**
3. Enter your credentials in the request body:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```
4. Click **"Execute"**
5. Copy the `access` token from the response

### Step 2: Authorize Swagger UI
1. Click the **"Authorize"** button at the top of the Swagger UI page
2. In the "Bearer" field, enter: `Bearer <your_access_token>`
   - Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. Click **"Authorize"**
4. Click **"Close"**

### Step 3: Test Authenticated Endpoints
- Now you can test any protected endpoint
- The JWT token will be automatically included in requests
- Tokens expire after 60 minutes (configured in settings)

## Features

### 1. Security Definitions
- **JWT Bearer Authentication** is configured
- Tokens are sent in the `Authorization` header
- Format: `Bearer <token>`

### 2. API Organization
All endpoints are organized by module:
- **Auth Module**: `/api/auth/`
- **Core Module**: `/api/core/`
- **Compliance Module**: `/api/compliance/`
- **Returns Module**: `/api/returns/`
- **Risk Assessment Module**: `/api/risk-assessment/`
- **Case Management Module**: `/api/case-management/`
- **VA/VASP Module**: `/api/va-vasp/`
- **Licensing Module**: `/api/licensing/`
- **SMI Module**: `/api/v1/`

### 3. Interactive Testing
- **Execute requests** directly from the browser
- **View responses** with status codes and headers
- **Download responses** as files
- **Copy curl commands** for terminal use

## Configuration

### Settings (config/settings.py)
```python
INSTALLED_APPS = [
    ...
    'drf_yasg',  # Swagger/OpenAPI documentation
    ...
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}
```

### URLs (config/urls.py)
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Prudential Regulatory Backend System API",
        default_version='v1',
        description="API documentation for the Prudential Regulatory Backend System (PRBS)",
        ...
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

## Tips and Best Practices

### 1. Testing Workflows
- Start with authentication endpoints
- Obtain and authorize with a token
- Test CRUD operations in sequence (Create → Read → Update → Delete)

### 2. Understanding Responses
- **200 OK**: Successful GET request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist

### 3. Exporting Documentation
- Use the **Download** button to get the OpenAPI spec
- Import into Postman: File → Import → Paste the swagger.json URL
- Share with frontend developers for API contract

### 4. Customizing Documentation
To improve your API documentation:
- Add docstrings to your ViewSets and Serializers
- Use `@swagger_auto_schema` decorator for custom documentation
- Define response schemas for better clarity

## Troubleshooting

### Issue: "Authentication credentials were not provided"
**Solution**: Make sure you've authorized with a valid JWT token

### Issue: "Token has expired"
**Solution**: Obtain a new token from `/api/auth/login/`

### Issue: Swagger UI not loading
**Solution**: 
- Check that `drf_yasg` is in `INSTALLED_APPS`
- Run `python manage.py collectstatic` if in production
- Verify URLs are correctly configured

### Issue: Endpoints not showing up
**Solution**:
- Ensure your ViewSets are registered in the app's `urls.py`
- Check that the app is included in the main `urls.py`
- Restart the development server

## Additional Resources

- **drf-yasg Documentation**: https://drf-yasg.readthedocs.io/
- **OpenAPI Specification**: https://swagger.io/specification/
- **Django REST Framework**: https://www.django-rest-framework.org/

## Support

For issues or questions about the API documentation, please contact the development team.
