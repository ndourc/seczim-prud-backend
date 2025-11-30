# Authentication Disabled - Production Deployment Guide

## ⚠️ IMPORTANT: Authentication has been disabled for this application

This document describes the changes made to disable authentication and how to deploy them to production.

## Changes Made

### 1. Global Settings Change
**File:** `config/settings.py`

Changed the default REST Framework permission class from `IsAuthenticated` to `AllowAny`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Changed from IsAuthenticated
    ],
    # ... other settings
}
```

### 2. View-Level Permission Changes
The following view files have been modified to use `AllowAny` permissions:

- `apps/core/views.py`
- `apps/auth_module/views.py`
- `apps/smi_module/views.py`

All `permission_classes` have been replaced with:
```python
permission_classes = [permissions.AllowAny]  # AUTH_DISABLED
```

### 3. Updated Scripts
- **`disable_auth.py`**: Enhanced to handle complex permission patterns
- **`restore_auth.py`**: Updated to restore original permissions when needed

## Deployment to Production (Render)

### Option 1: Deploy via Git Push (Recommended)

1. **Commit the changes:**
   ```bash
   git add .
   git commit -m "Disable authentication for production"
   ```

2. **Push to main branch:**
   ```bash
   git push origin main
   ```

3. **Render will automatically deploy:**
   - Render monitors the `main` branch (as configured in `render.yaml`)
   - Once you push, Render will automatically build and deploy
   - Monitor the deployment at: https://dashboard.render.com/

### Option 2: Manual Deploy via Render Dashboard

1. Go to https://dashboard.render.com/
2. Select your `prudential-backend` service
3. Click "Manual Deploy" → "Deploy latest commit"

## Verification Steps

After deployment, verify that authentication is disabled:

1. **Test an endpoint without authentication:**
   ```bash
   curl https://your-app.onrender.com/api/core/smis/
   ```
   
   You should receive data without needing to provide an Authorization header.

2. **Check Swagger UI:**
   - Visit: `https://your-app.onrender.com/swagger/`
   - Try endpoints without clicking "Authorize"
   - All endpoints should work without authentication

3. **Test from your frontend:**
   - Remove JWT token from API requests
   - All API calls should work without authentication

## Security Considerations

⚠️ **WARNING:** With authentication disabled:
- All API endpoints are publicly accessible
- Anyone can read, create, update, and delete data
- There is NO user-level data isolation
- This configuration is NOT recommended for production with sensitive data

## Restoring Authentication

If you need to re-enable authentication:

1. **Run the restore script:**
   ```bash
   python restore_auth.py
   ```

2. **Manually update `config/settings.py`:**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```

3. **Commit and deploy:**
   ```bash
   git add .
   git commit -m "Restore authentication"
   git push origin main
   ```

## Environment Variables

The following environment variables are configured in Render (from `render.yaml`):
- `SECRET_KEY`: Auto-generated
- `DEBUG`: False
- `ALLOWED_HOSTS`: Configure as needed
- `DJANGO_SETTINGS_MODULE`: config.settings
- `PYTHON_VERSION`: 3.11.0

## Monitoring

After deployment:
1. Check Render logs for any errors
2. Monitor the health check endpoint: `/admin/`
3. Test critical API endpoints

## Rollback Plan

If issues occur after deployment:

1. **Quick rollback via Render:**
   - Go to Render Dashboard
   - Select your service
   - Click "Rollback" to previous deployment

2. **Or revert via Git:**
   ```bash
   git revert HEAD
   git push origin main
   ```

## Support

If you encounter issues:
1. Check Render deployment logs
2. Review Django application logs
3. Verify all environment variables are set correctly
4. Ensure database migrations have run successfully

---

**Last Updated:** 2025-11-30
**Status:** Authentication Disabled ✅
