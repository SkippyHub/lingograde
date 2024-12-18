import React, { useState, useEffect } from 'react';
import { AudioRecorder } from './AudioRecorder';
import { RecordingsList } from './RecordingsList';
import { useApi } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { Recording } from '../types';
import { Link } from 'react-router-dom';

const SPEAKING_PROMPTS = [
  "Describe your ideal vacation destination and explain why you would choose to visit that place.",
  "What is your favorite hobby and why do you enjoy it?",
  "Tell me about a memorable experience from your childhood.",
  "If you could have dinner with any historical figure, who would it be and why?",
  "What do you think will be the most significant technological advancement in the next 10 years?",
  "Describe a challenge you've overcome and what you learned from it.",
  "What advice would you give to someone learning a new language?",
  "If you could instantly master any skill, what would it be and why?",
];

export const Dashboard: React.FC = () => {
  const { logout } = useAuth();
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recordingError, setRecordingError] = useState<string | null>(null);
  const api = useApi();
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);

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
      setRecordingError(null);
      await api.analyzeAudio(audioBlob, SPEAKING_PROMPTS[currentPromptIndex]);
      await checkApiAndLoadRecordings();
    } catch (error) {
      console.error('Failed to analyze audio:', error);
      setRecordingError('Unable to record audio. Please check your microphone permissions and try again.');
    }
  };

  const getNextPrompt = () => {
    setCurrentPromptIndex((prev) => (prev + 1) % SPEAKING_PROMPTS.length);
  };

  return (
    <div className="min-h-screen animated-gradient relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/90 via-white/50 to-orange-100/70 pointer-events-none" />
      <div className="relative">
        <nav className="bg-white/70 backdrop-blur-sm shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <Link to="/" className="text-3xl font-extrabold text-gray-900">
                <span className="text-indigo-600">LingoGrade</span>
              </Link>
              <button
                onClick={logout}
                className="px-8 py-3 text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 border border-indigo-600"
              >
                Logout
              </button>
            </div>
          </div>
        </nav>

        {error && (
          <div className="max-w-7xl mx-auto px-4 py-2 mt-2">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          </div>
        )}

        {recordingError && (
          <div className="max-w-7xl mx-auto px-4 py-2 mt-2">
            <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded-md" role="alert">
              <strong className="font-bold">Recording Error: </strong>
              <span className="block sm:inline">{recordingError}</span>
            </div>
          </div>
        )}

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Recording List Section - Full width on small/medium, 2/3 on large */}
            <div className="order-2 lg:order-1 lg:col-span-2">
              {isLoading ? (
                <div className="bg-white rounded-lg shadow px-6 py-8">
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

            {/* Recording Section - Full width on small/medium, 1/3 on large */}
            <div className="order-1 lg:order-2 lg:col-span-1">
              <div className="bg-white rounded-lg shadow px-6 pb-8 pt-8">
                <div className="relative">
                  <div className="absolute -top-10 left-6">
                    <div className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
                      <span className="h-full w-full flex items-center justify-center text-2xl">🎙️</span>
                    </div>
                  </div>
                  <h2 className="text-lg font-medium text-gray-900 tracking-tight pt-4">Record Speech</h2>
                  
                  <div className="mt-4 p-4 bg-indigo-50 rounded-lg border border-indigo-100">
                    <div className="flex items-start space-x-2">
                      <span className="text-xl">💭</span>
                      <div>
                        <h3 className="text-sm font-medium text-indigo-800">Speaking Prompt:</h3>
                        <p className="text-sm text-indigo-600 mt-1">
                          "{SPEAKING_PROMPTS[currentPromptIndex]}"
                        </p>
                        <button
                          onClick={getNextPrompt}
                          className="mt-2 text-xs text-indigo-500 hover:text-indigo-600 flex items-center"
                        >
                          <span>Next prompt</span>
                          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 flex flex-col items-center">
                    <div className="relative">
                      <svg className="w-24 h-24" viewBox="0 0 100 100">
                        <circle 
                          cx="50" 
                          cy="50" 
                          r="45" 
                          fill="none" 
                          stroke="currentColor" 
                          strokeWidth="2" 
                          className="text-gray-200"
                        />
                        <circle 
                          cx="50" 
                          cy="50" 
                          r="45" 
                          fill="none" 
                          stroke="currentColor" 
                          strokeWidth="3" 
                          className="text-indigo-500 transform scale-0 transition-transform duration-300 recording:scale-100"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-4xl">🎙️</span>
                      </div>
                    </div>
                    <AudioRecorder onRecordingComplete={handleNewRecording} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}; 