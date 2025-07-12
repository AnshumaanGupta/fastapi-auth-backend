// Frontend API Integration Guide for React
// File: src/services/authService.js

const API_BASE_URL = 'http://209.38.123.128/api/auth';

// Auth Service Class
class AuthService {
  
  // Helper method for making API requests
  async makeRequest(endpoint, options = {}) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
      }

      return data;
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  // 1. SIGNUP - Register a new user
  async signup(userData) {
    return this.makeRequest('/signup', {
      method: 'POST',
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        first_name: userData.firstName,
        last_name: userData.lastName,
      }),
    });
  }

  // 2. SIGNIN - Login user and get JWT token
  async signin(credentials) {
    const response = await this.makeRequest('/signin', {
      method: 'POST',
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    // Store token in localStorage
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }

    return response;
  }

  // 3. FORGOT PASSWORD - Request password reset
  async forgotPassword(email) {
    return this.makeRequest('/forgot-password', {
      method: 'POST',
      body: JSON.stringify({
        email: email,
      }),
    });
  }

  // 4. RESET PASSWORD - Reset password with token
  async resetPassword(token, newPassword) {
    return this.makeRequest('/reset-password', {
      method: 'POST',
      body: JSON.stringify({
        token: token,
        new_password: newPassword,
      }),
    });
  }

  // 5. GET USER INFO - Get current user (protected route)
  async getCurrentUser() {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No token found');
    }

    return this.makeRequest('/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  }

  // 6. VERIFY TOKEN - Check if token is valid
  async verifyToken() {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return false;
    }

    try {
      await this.makeRequest('/verify-token', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      return true;
    } catch {
      return false;
    }
  }

  // 7. LOGOUT - Clear local storage
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  // 8. GET TOKEN - Get stored token
  getToken() {
    return localStorage.getItem('access_token');
  }

  // 9. GET USER - Get stored user
  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  // 10. IS AUTHENTICATED - Check if user is logged in
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }
}

// Export singleton instance
export default new AuthService();
