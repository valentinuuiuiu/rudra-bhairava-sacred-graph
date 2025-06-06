# Google OAuth Setup Guide for Piata.ro

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Piata RO Marketplace"
4. Click "Create"

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

## Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (for testing with any Google account)
3. Fill in the required fields:
   - **App name**: Piata.ro Marketplace
   - **User support email**: Your email
   - **Developer contact information**: Your email
4. Click "Save and Continue"
5. Skip "Scopes" → Click "Save and Continue"
6. Add test users (your email and any others you want to test with)
7. Click "Save and Continue"

## Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Enter name: "Piata.ro Web Client"
5. Add Authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - (Add your production domain later: `https://yourdomain.com/accounts/google/login/callback/`)
6. Click "Create"
7. **Copy the Client ID and Client Secret** - you'll need these!

## Step 5: Configure Django

After getting your credentials, you'll need to:

1. Add them to Django admin as a Social Application
2. Or use environment variables (recommended for production)

### Method 1: Django Admin (Easier for development)

1. Start your Django server: `python manage.py runserver`
2. Go to: `http://localhost:8000/admin/`
3. Login with your superuser account
4. Go to "Social Applications" → "Add social application"
5. Fill in:
   - **Provider**: Google
   - **Name**: Google
   - **Client id**: [Your Google Client ID]
   - **Secret key**: [Your Google Client Secret]
   - **Sites**: Select "example.com" (or add your site)
6. Save

### Method 2: Environment Variables (Recommended)

Create a `.env` file in your project root:

```bash
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

Then update settings.py to use these variables.

## Step 6: Test the Integration

1. Restart your Django server
2. Go to the login page
3. Click "Continue with Google"
4. You should be redirected to Google's login page
5. After authentication, you'll be redirected back to your site

## Troubleshooting

- **Error 400: redirect_uri_mismatch**: Check that your redirect URIs in Google Console match exactly
- **Error 403: access_blocked**: Make sure your app is in "Testing" mode and you've added test users
- **Social Application not found**: Make sure you've created the Social Application in Django admin

## Production Considerations

- Use environment variables for credentials
- Add your production domain to authorized redirect URIs
- Consider setting up proper SSL certificates
- Review and update OAuth consent screen for production use
