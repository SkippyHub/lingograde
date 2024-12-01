import React, { useState, useEffect } from 'react';
import { AudioRecorder } from './AudioRecorder';
import { RecordingsList } from './RecordingsList';
import { useApi } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { Recording } from '../types';

export const Dashboard: React.FC = () => {
  const { logout } = useAuth();
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const api = useApi();

  useEffect(() => {
    checkApiAndLoadRecordings();
  }, []);

  const checkApiAndLoadRecordings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getRecordings();
      setRecordings(data);
    } catch (error) {
      console.error('API check failed:', error);
      setError('Failed to connect to the server. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewRecording = async (audioBlob: Blob) => {
    try {
      setError(null);
      await api.analyzeAudio(audioBlob);
      await checkApiAndLoadRecordings();
    } catch (error) {
      console.error('Failed to analyze audio:', error);
      setError('Failed to analyze audio. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">LingoGrade</h1>
          <button
            onClick={logout}
            className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
          >
            Logout
          </button>
        </div>
      </nav>

      {error && (
        <div className="max-w-7xl mx-auto px-4 py-2 mt-2">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        </div>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-3 gap-8">
          <div className="col-span-2">
            <div className="bg-white rounded-lg shadow p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">Record Speech</h2>
              <AudioRecorder onRecordingComplete={handleNewRecording} />
            </div>
          </div>
          <div className="col-span-1">
            {isLoading ? (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-4 py-1">
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div className="space-y-2">
                      <div className="h-4 bg-gray-200 rounded"></div>
                      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <RecordingsList 
                recordings={recordings} 
                onAudioRequest={api.getRecordingAudio}
                onRecordingsUpdate={setRecordings}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}; 