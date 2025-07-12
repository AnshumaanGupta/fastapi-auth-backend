// Example Dashboard Component
// File: src/components/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import authService from '../services/authService';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserInfo();
  }, []);

  const fetchUserInfo = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUserInfo(userData);
    } catch (error) {
      console.error('Failed to fetch user info:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Welcome to Dashboard</h1>
      
      <div className="user-info">
        <h3>User Information</h3>
        <p><strong>Name:</strong> {userInfo?.first_name} {userInfo?.last_name}</p>
        <p><strong>Email:</strong> {userInfo?.email}</p>
        <p><strong>Account Created:</strong> {new Date(userInfo?.created_at).toLocaleDateString()}</p>
        <p><strong>Verified:</strong> {userInfo?.is_verified ? 'Yes' : 'No'}</p>
      </div>

      <button onClick={handleLogout} className="logout-btn">
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
