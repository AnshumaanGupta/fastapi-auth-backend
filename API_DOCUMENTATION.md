# Authentication API Documentation

## Base URL
```
http://209.38.123.128
```

## API Version
```
v1.0.0
```

## Content Type
All requests must include:
```
Content-Type: application/json
```

## Authentication
Protected endpoints require JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 📋 Table of Contents

1. [Health Check](#health-check)
2. [User Registration (Signup)](#user-registration-signup)
3. [User Authentication (Signin)](#user-authentication-signin)
4. [Forgot Password](#forgot-password)
5. [Reset Password](#reset-password)
6. [Get Current User](#get-current-user-protected)
7. [Verify Token](#verify-token-protected)
8. [Error Responses](#error-responses)
9. [Status Codes](#status-codes)

---

## Health Check

### `GET /health`

Check if the API server is running.

#### Request
```http
GET http://209.38.123.128/health
```

#### Response
```json
{
  "status": "healthy"
}
```

#### Status Codes
- `200 OK` - Server is healthy

---

## User Registration (Signup)

### `POST /api/auth/signup`

Register a new user account.

#### Request
```http
POST http://209.38.123.128/api/auth/signup
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Request Body Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | Valid email address |
| `password` | string | ✅ | Minimum 6 characters |
| `first_name` | string | ✅ | User's first name |
| `last_name` | string | ✅ | User's last name |

#### Success Response
```json
{
  "message": "User created successfully. Please sign in.",
  "success": true
}
```

#### Error Response
```json
{
  "detail": "Email already registered"
}
```

#### Status Codes
- `200 OK` - User created successfully
- `400 Bad Request` - Email already exists or validation error
- `422 Unprocessable Entity` - Invalid email format
- `500 Internal Server Error` - Server error

#### Example cURL
```bash
curl -X POST http://209.38.123.128/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securePassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

---

## User Authentication (Signin)

### `POST /api/auth/signin`

Authenticate user and receive JWT token.

#### Request
```http
POST http://209.38.123.128/api/auth/signin
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securePassword123"
}
```

#### Request Body Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | User's email address |
| `password` | string | ✅ | User's password |

#### Success Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2025-07-12T10:30:00Z",
    "is_verified": false
  }
}
```

#### Response Schema
| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT token for authentication |
| `token_type` | string | Always "bearer" |
| `user.id` | string | Unique user ID (UUID) |
| `user.email` | string | User's email |
| `user.first_name` | string | User's first name |
| `user.last_name` | string | User's last name |
| `user.created_at` | string | Account creation timestamp (ISO 8601) |
| `user.is_verified` | boolean | Email verification status |

#### Error Response
```json
{
  "detail": "Invalid email or password"
}
```

#### Status Codes
- `200 OK` - Authentication successful
- `401 Unauthorized` - Invalid credentials
- `422 Unprocessable Entity` - Invalid email format

#### Example cURL
```bash
curl -X POST http://209.38.123.128/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securePassword123"
  }'
```

---

## Forgot Password

### `POST /api/auth/forgot-password`

Request a password reset email.

#### Request
```http
POST http://209.38.123.128/api/auth/forgot-password
Content-Type: application/json

{
  "email": "john.doe@example.com"
}
```

#### Request Body Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | User's email address |

#### Success Response
```json
{
  "message": "If the email exists, a password reset link has been sent.",
  "success": true
}
```

#### Status Codes
- `200 OK` - Request processed (always returns success for security)
- `422 Unprocessable Entity` - Invalid email format
- `500 Internal Server Error` - Failed to send email

#### Example cURL
```bash
curl -X POST http://209.38.123.128/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com"
  }'
```

---

## Reset Password

### `POST /api/auth/reset-password`

Reset password using the token from email.

#### Request
```http
POST http://209.38.123.128/api/auth/reset-password
Content-Type: application/json

{
  "token": "abc123def456ghi789jkl012mno345",
  "new_password": "newSecurePassword123"
}
```

#### Request Body Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | ✅ | Reset token from email |
| `new_password` | string | ✅ | New password (minimum 6 characters) |

#### Success Response
```json
{
  "message": "Password updated successfully",
  "success": true
}
```

#### Error Response
```json
{
  "detail": "Invalid or expired reset token"
}
```

#### Status Codes
- `200 OK` - Password updated successfully
- `400 Bad Request` - Invalid or expired token
- `500 Internal Server Error` - Failed to update password

#### Example cURL
```bash
curl -X POST http://209.38.123.128/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "abc123def456ghi789jkl012mno345",
    "new_password": "newSecurePassword123"
  }'
```

---

## Get Current User (Protected)

### `GET /api/auth/me`

Get current authenticated user information.

#### Request
```http
GET http://209.38.123.128/api/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Success Response
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2025-07-12T10:30:00Z",
  "is_verified": false
}
```

#### Error Response
```json
{
  "detail": "Invalid token"
}
```

#### Status Codes
- `200 OK` - User information retrieved
- `401 Unauthorized` - Invalid or missing token
- `404 Not Found` - User not found

#### Example cURL
```bash
curl -X GET http://209.38.123.128/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Verify Token (Protected)

### `POST /api/auth/verify-token`

Verify if the provided JWT token is valid.

#### Request
```http
POST http://209.38.123.128/api/auth/verify-token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Success Response
```json
{
  "message": "Token is valid",
  "success": true
}
```

#### Error Response
```json
{
  "detail": "Invalid token"
}
```

#### Status Codes
- `200 OK` - Token is valid
- `401 Unauthorized` - Invalid or expired token

#### Example cURL
```bash
curl -X POST http://209.38.123.128/api/auth/verify-token \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common Error Messages

| Error | Description |
|-------|-------------|
| `Email already registered` | User tried to signup with existing email |
| `Invalid email or password` | Login failed due to wrong credentials |
| `Invalid token` | JWT token is invalid or expired |
| `Invalid or expired reset token` | Password reset token is invalid |
| `User not found` | User account doesn't exist |
| `Failed to create user` | Server error during registration |
| `Failed to send reset email` | SMTP configuration issue |

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid request data |
| `401` | Unauthorized | Authentication required or failed |
| `404` | Not Found | Resource not found |
| `422` | Unprocessable Entity | Validation error |
| `500` | Internal Server Error | Server error |

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

---

## CORS

The API supports CORS for the following origins:
- `http://localhost:3000` (React development)
- `http://209.38.123.128` (Production frontend)

---

## Interactive API Documentation

Visit the interactive API documentation:
```
http://209.38.123.128/docs
```

This provides a Swagger UI where you can:
- See all available endpoints
- Test API calls directly
- View request/response schemas
- Download OpenAPI specification

---

## Authentication Flow Example

### 1. Register User
```javascript
const response = await fetch('http://209.38.123.128/api/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123',
    first_name: 'John',
    last_name: 'Doe'
  })
});
```

### 2. Login User
```javascript
const response = await fetch('http://209.38.123.128/api/auth/signin', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access_token, user } = await response.json();
```

### 3. Make Protected Request
```javascript
const response = await fetch('http://209.38.123.128/api/auth/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const userInfo = await response.json();
```

---

## Security Considerations

1. **HTTPS**: Use HTTPS in production
2. **Token Storage**: Store JWT tokens securely (avoid localStorage for sensitive apps)
3. **Token Expiry**: Tokens expire after 30 minutes
4. **Password Policy**: Minimum 6 characters (consider stronger requirements)
5. **Rate Limiting**: Implement rate limiting for production
6. **Input Validation**: All inputs are validated server-side

---

## Support

For issues or questions:
- Check server logs: `ssh root@209.38.123.128 "journalctl -u backendauth -f"`
- Restart service: `ssh root@209.38.123.128 "systemctl restart backendauth"`
- API Health: `http://209.38.123.128/health`
