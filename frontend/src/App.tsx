import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
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
      {isAuthenticated ? (
        <>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
          <Route path="/recordings" element={<RecordingsList 
            recordings={recordings}
            onAudioRequest={handleAudioRequest}
            onRecordingsUpdate={handleRecordingsUpdate}
          />} />
        </>
      ) : (
        <>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </>
      )}
    </Routes>
  );
} 