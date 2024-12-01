import { useState } from 'react';
import { Navigate, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import { Login } from './components/Login';
import { Signup } from './components/Signup';
import { Dashboard } from './components/Dashboard';
import { useAuth } from './contexts/AuthContext';
import { Recording } from './types';
import { RecordingsList } from './components/RecordingsList';
import { useApi } from './api';

export default function App() {
  const { isAuthenticated, loading } = useAuth();
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const api = useApi();

  const handleAudioRequest = async (filename: string) => {
    return await api.getRecordingAudio(filename);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  const handleRecordingsUpdate = (newRecordings: Recording[]) => {
    setRecordings(newRecordings);
  };

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} 
      />
      <Route 
        path="/signup" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Signup />} 
      />
      <Route 
        path="/dashboard" 
        element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />} 
      />
      <Route 
        path="/recordings" 
        element={
          isAuthenticated ? (
            <RecordingsList 
              recordings={recordings}
              onAudioRequest={handleAudioRequest}
              onRecordingsUpdate={handleRecordingsUpdate}
            />
          ) : (
            <Navigate to="/login" replace />
          )
        } 
      />
      <Route 
        path="*" 
        element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
      />
    </Routes>
  );
} 