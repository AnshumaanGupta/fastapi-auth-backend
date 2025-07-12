# Backend Authentication API

A Python FastAPI backend for user authentication with email/password login, signup, and password reset functionality using Supabase as the database.

## Features

- User Registration (Sign Up)
- User Authentication (Sign In)
- Password Reset via Email
- JWT Token-based Authentication
- Protected Routes
- CORS enabled for React frontend
- Supabase Database Integration

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database and authentication
- **JWT** - JSON Web Tokens for authentication
- **Passlib** - Password hashing
- **Python-Jose** - JWT token handling
- **SMTP** - Email sending for password reset

## Project Structure

```
backendauth/
├── main.py                 # FastAPI application entry point
├── schemas.py              # Pydantic models
├── database.py             # Supabase connection
├── auth_utils.py           # Authentication utilities
├── routes/
│   ├── __init__.py
│   └── auth.py             # Authentication routes
├── requirements.txt        # Python dependencies
├── supabase_schema.sql     # Database schema
├── .env.example           # Environment variables template
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Navigate to your project directory
cd backendauth

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Settings > API to get your URL and anon key
3. Go to SQL Editor and run the schema from `supabase_schema.sql`

### 3. Environment Configuration

1. Copy `.env.example` to `.env`:

   ```bash
   copy .env.example .env
   ```

2. Fill in your environment variables in `.env`:

   ```env
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key

   # JWT Configuration
   SECRET_KEY=your_very_long_random_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Email Configuration
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password

   # Frontend URL
   FRONTEND_URL=http://localhost:3000
   ```

### 4. Generate Secret Key

Generate a secure secret key for JWT:

```python
import secrets
print(secrets.token_urlsafe(32))
```

### 5. Email Configuration (Gmail Example)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `SMTP_PASSWORD`

## Running the Application

```bash
# Make sure virtual environment is activated
# Run the application
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication Routes (Prefix: `/api/auth`)

| Method | Endpoint           | Description                          |
| ------ | ------------------ | ------------------------------------ |
| POST   | `/signup`          | Register a new user                  |
| POST   | `/signin`          | Authenticate user and get token      |
| POST   | `/forgot-password` | Request password reset email         |
| POST   | `/reset-password`  | Reset password with token            |
| GET    | `/me`              | Get current user info (protected)    |
| POST   | `/verify-token`    | Verify if token is valid (protected) |

### Request/Response Examples

#### Sign Up

```json
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Sign In

```json
POST /api/auth/signin
{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2025-01-01T00:00:00",
    "is_verified": false
  }
}
```

#### Forgot Password

```json
POST /api/auth/forgot-password
{
  "email": "user@example.com"
}
```

#### Reset Password

```json
POST /api/auth/reset-password
{
  "token": "reset_token_from_email",
  "new_password": "newpassword123"
}
```

## Frontend Integration (React)

### Authentication Context Example

```javascript
// Example of how to integrate with React
const API_BASE_URL = "http://localhost:8000/api/auth";

// Sign Up
const signUp = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  return response.json();
};

// Sign In
const signIn = async (credentials) => {
  const response = await fetch(`${API_BASE_URL}/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  return response.json();
};

// Protected API calls
const makeAuthenticatedRequest = async (url, options = {}) => {
  const token = localStorage.getItem("access_token");
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
};
```

## Database Schema

The application uses two main tables:

### Users Table

- `id`: UUID (Primary Key)
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `first_name`: User's first name
- `last_name`: User's last name
- `is_verified`: Email verification status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Password Resets Table

- `id`: UUID (Primary Key)
- `email`: Email for password reset
- `token`: Unique reset token
- `expires_at`: Token expiration time (1 hour)
- `used`: Whether token has been used
- `created_at`: Token creation timestamp

## Security Features

- Password hashing using bcrypt
- JWT tokens with expiration
- CORS configuration
- Rate limiting (can be added with slowapi)
- Email verification tokens
- Secure password reset flow

## Production Deployment

1. Set secure environment variables
2. Use a production WSGI server like Gunicorn
3. Set up HTTPS
4. Configure proper CORS origins
5. Add rate limiting
6. Set up monitoring and logging
7. Use a production database

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload
```

## Testing

You can test the API using:

- FastAPI automatic docs at `/docs`
- Postman or similar API testing tools
- Python requests library
- Your React frontend

## License

This project is open source and available under the MIT License.
