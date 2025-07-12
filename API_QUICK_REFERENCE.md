# API Quick Reference

## Base URL
```
http://209.38.123.128
```

## Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/health` | ❌ | Health check |
| GET | `/` | ❌ | API status |
| POST | `/api/auth/signup` | ❌ | Register user |
| POST | `/api/auth/signin` | ❌ | Login user |
| POST | `/api/auth/forgot-password` | ❌ | Request password reset |
| POST | `/api/auth/reset-password` | ❌ | Reset password with token |
| GET | `/api/auth/me` | ✅ | Get current user |
| POST | `/api/auth/verify-token` | ✅ | Verify JWT token |

## Quick Examples

### Signup
```bash
curl -X POST http://209.38.123.128/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","first_name":"Test","last_name":"User"}'
```

### Signin
```bash
curl -X POST http://209.38.123.128/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

### Get User (Protected)
```bash
curl -X GET http://209.38.123.128/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Forgot Password
```bash
curl -X POST http://209.38.123.128/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

## JavaScript Examples

### Using Fetch API
```javascript
// Signup
const signup = await fetch('http://209.38.123.128/api/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123',
    first_name: 'John',
    last_name: 'Doe'
  })
});

// Signin
const signin = await fetch('http://209.38.123.128/api/auth/signin', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access_token, user } = await signin.json();

// Protected request
const userInfo = await fetch('http://209.38.123.128/api/auth/me', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## Common Response Formats

### Success Response (Signup/Forgot Password)
```json
{
  "message": "Success message",
  "success": true
}
```

### Token Response (Signin)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2025-07-12T10:30:00Z",
    "is_verified": false
  }
}
```

### User Response (Get User)
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2025-07-12T10:30:00Z",
  "is_verified": false
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

## Status Codes
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error
