# Frontend Integration Guide

## 🚀 Complete React Frontend Integration for Authentication API

This guide shows you how to integrate your deployed authentication backend (`http://209.38.123.128`) with a React frontend.

## 📁 Project Structure

```
src/
├── services/
│   └── authService.js          # API calls service
├── contexts/
│   └── AuthContext.jsx         # Authentication state management
├── components/
│   ├── auth/
│   │   ├── SignupForm.jsx      # User registration
│   │   ├── SigninForm.jsx      # User login
│   │   ├── ForgotPasswordForm.jsx  # Password reset request
│   │   ├── ResetPasswordForm.jsx   # Password reset with token
│   │   └── ProtectedRoute.jsx  # Route protection
│   └── Dashboard.jsx           # Protected dashboard
├── App.jsx                     # Main app with routing
└── App.css                     # Styling
```

## 🛠️ Installation

Install required dependencies:

```bash
npm install react-router-dom
```

## 📋 Usage Examples

### 1. **Signup (Registration)**

```javascript
import authService from './services/authService';

const handleSignup = async () => {
  try {
    const response = await authService.signup({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      password: 'password123'
    });
    console.log('Account created!', response);
  } catch (error) {
    console.error('Signup failed:', error.message);
  }
};
```

### 2. **Signin (Login)**

```javascript
const handleSignin = async () => {
  try {
    const response = await authService.signin({
      email: 'john@example.com',
      password: 'password123'
    });
    console.log('Logged in!', response.user);
    // Token is automatically stored in localStorage
  } catch (error) {
    console.error('Login failed:', error.message);
  }
};
```

### 3. **Forgot Password**

```javascript
const handleForgotPassword = async () => {
  try {
    const response = await authService.forgotPassword('john@example.com');
    console.log('Reset email sent!', response);
  } catch (error) {
    console.error('Failed to send reset email:', error.message);
  }
};
```

### 4. **Reset Password**

```javascript
const handleResetPassword = async (token, newPassword) => {
  try {
    const response = await authService.resetPassword(token, newPassword);
    console.log('Password updated!', response);
  } catch (error) {
    console.error('Password reset failed:', error.message);
  }
};
```

### 5. **Protected API Calls**

```javascript
const fetchUserData = async () => {
  try {
    const user = await authService.getCurrentUser();
    console.log('Current user:', user);
  } catch (error) {
    console.error('Failed to fetch user:', error.message);
  }
};
```

## 🔒 Authentication Flow

1. **User Registration**: `SignupForm.jsx` → API → Success message
2. **User Login**: `SigninForm.jsx` → API → Store token → Redirect to dashboard
3. **Protected Routes**: Check token → Allow/Deny access
4. **Password Reset**: Email form → API → Email sent → Reset form → Success

## 🎨 Styling

Basic CSS is provided in `App.css`. You can customize it or use your preferred CSS framework:

- **Tailwind CSS**: For utility-first styling
- **Material-UI**: For Material Design components
- **Bootstrap**: For responsive components

## 🚀 Quick Start

1. **Copy the files** to your React project
2. **Update the API URL** in `authService.js` (already set to your droplet)
3. **Install dependencies**: `npm install react-router-dom`
4. **Import and use** the components in your app

## 🔧 Configuration

### Environment Variables (optional)

Create a `.env` file in your React project root:

```env
REACT_APP_API_BASE_URL=http://209.38.123.128/api/auth
```

Update `authService.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://209.38.123.128/api/auth';
```

## 📱 Mobile Considerations

For React Native, replace `localStorage` with `AsyncStorage`:

```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Replace localStorage.setItem with:
await AsyncStorage.setItem('access_token', token);

// Replace localStorage.getItem with:
const token = await AsyncStorage.getItem('access_token');
```

## 🛡️ Security Best Practices

1. **HTTPS**: Use HTTPS in production
2. **Token Expiry**: Handle token expiration gracefully
3. **Input Validation**: Validate all user inputs
4. **Error Handling**: Don't expose sensitive error details
5. **CORS**: Configure CORS properly on your backend

## 🧪 Testing

Test your API calls:

```javascript
// Test signup
authService.signup({
  firstName: 'Test',
  lastName: 'User',
  email: 'test@example.com',
  password: 'password123'
});

// Test signin
authService.signin({
  email: 'test@example.com',
  password: 'password123'
});
```

## 🔗 API Endpoints

Your backend is available at: `http://209.38.123.128`

- **Signup**: `POST /api/auth/signup`
- **Signin**: `POST /api/auth/signin`
- **Forgot Password**: `POST /api/auth/forgot-password`
- **Reset Password**: `POST /api/auth/reset-password`
- **Get User**: `GET /api/auth/me`
- **Verify Token**: `POST /api/auth/verify-token`

## 📚 Next Steps

1. **Email Configuration**: Set up SMTP for password reset emails
2. **Email Verification**: Add email verification flow
3. **User Profiles**: Extend user management features
4. **Role-based Access**: Add user roles and permissions
5. **Social Login**: Integrate Google/Facebook login

Your authentication system is now ready for production use! 🎉
