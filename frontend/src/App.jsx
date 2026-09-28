import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AIChatPage from './pages/AIChatPage';
import DisasterInfoPage from './pages/DisasterInfoPage';
import ChecklistPage from './pages/ChecklistPage';
import EmergencyServicesPage from './pages/EmergencyServicesPage';
import AlertsPage from './pages/AlertsPage';
import HistoryPage from './pages/HistoryPage';
import ProfilePage from './pages/ProfilePage';
import AdminDashboardPage from './pages/AdminDashboardPage';

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/chat" element={<AIChatPage />} />
          <Route path="/disasters" element={<DisasterInfoPage />} />
          <Route path="/disasters/:type" element={<DisasterInfoPage />} />
          <Route path="/checklist" element={<ChecklistPage />} />
          <Route path="/emergency-services" element={<EmergencyServicesPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/alerts/:id" element={<AlertsPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/admin" element={<AdminDashboardPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
