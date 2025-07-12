# Postman Collection for Authentication API

## Import Instructions
1. Open Postman
2. Click "Import" 
3. Copy and paste this JSON
4. Set the `{{base_url}}` variable to `http://209.38.123.128`

```json
{
  "info": {
    "name": "Authentication API",
    "description": "Complete authentication API for user management",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://209.38.123.128",
      "type": "string"
    },
    {
      "key": "jwt_token",
      "value": "",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      },
      "response": []
    },
    {
      "name": "API Status",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/",
          "host": ["{{base_url}}"],
          "path": [""]
        }
      },
      "response": []
    },
    {
      "name": "User Signup",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\",\n  \"first_name\": \"Test\",\n  \"last_name\": \"User\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/auth/signup",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "signup"]
        }
      },
      "response": []
    },
    {
      "name": "User Signin",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "// Extract JWT token from response",
              "if (pm.response.code === 200) {",
              "    const response = pm.response.json();",
              "    pm.collectionVariables.set('jwt_token', response.access_token);",
              "    console.log('JWT Token saved:', response.access_token);",
              "}"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/auth/signin",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "signin"]
        }
      },
      "response": []
    },
    {
      "name": "Get Current User",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{jwt_token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/auth/me",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "me"]
        }
      },
      "response": []
    },
    {
      "name": "Verify Token",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{jwt_token}}"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/auth/verify-token",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "verify-token"]
        }
      },
      "response": []
    },
    {
      "name": "Forgot Password",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/auth/forgot-password",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "forgot-password"]
        }
      },
      "response": []
    },
    {
      "name": "Reset Password",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"token\": \"RESET_TOKEN_FROM_EMAIL\",\n  \"new_password\": \"newPassword123\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/auth/reset-password",
          "host": ["{{base_url}}"],
          "path": ["api", "auth", "reset-password"]
        }
      },
      "response": []
    }
  ]
}
```

## Test Sequence

1. **Health Check** - Verify API is running
2. **User Signup** - Create a test account
3. **User Signin** - Login and get JWT token (automatically saved)
4. **Get Current User** - Test protected endpoint
5. **Verify Token** - Validate JWT token
6. **Forgot Password** - Request password reset
7. **Reset Password** - Reset with token from email

## Variables Setup

In Postman, set these collection variables:
- `base_url`: `http://209.38.123.128`
- `jwt_token`: (automatically set after signin)

## Environment Variables (Alternative)

Create a Postman environment with:
```json
{
  "name": "Authentication API Environment",
  "values": [
    {
      "key": "base_url",
      "value": "http://209.38.123.128",
      "enabled": true
    },
    {
      "key": "jwt_token",
      "value": "",
      "enabled": true
    },
    {
      "key": "test_email",
      "value": "test@example.com",
      "enabled": true
    },
    {
      "key": "test_password",
      "value": "password123",
      "enabled": true
    }
  ]
}
```
