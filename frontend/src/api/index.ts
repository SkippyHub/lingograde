import { useAuth } from '../contexts/AuthContext';

interface Api {
  getRecordings: () => Promise<any>;
  analyzeAudio: (audioBlob: Blob, prompt: string) => Promise<any>;
  getRecordingAudio: (filename: string) => Promise<Blob>;
  delete: (path: string) => Promise<any>;
  get: (path: string) => Promise<any>;
}

export const useApi = () => {
  const { token } = useAuth();

  const headers = {
    'Authorization': `Bearer ${token}`,
  };

  const getRecordings = async () => {
    const response = await fetch(`/api/recordings`, {
      headers,
    });
    if (!response.ok) throw new Error('Failed to fetch recordings');
    return response.json();
  };

  const analyzeAudio = async (audioBlob: Blob, prompt: string) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('prompt', prompt);

    const response = await fetch(`/api/analyze-audio`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) throw new Error('Failed to analyze audio');
    return response.json();
  };

  const getRecordingAudio = async (filename: string) => {
    const response = await fetch(`/api/recordings/${filename}`, {
      headers,
    });
    if (!response.ok) throw new Error('Failed to fetch audio');
    return response.blob();
  };

  const deleteRecording = async (path: string) => {
    const response = await fetch(`/api${path}`, {
      method: 'DELETE',
      headers,
    });
    return response;
  };

  const get = async (path: string) => {
    const response = await fetch(`/api${path}`, {
      headers,
    });
    return response.json();
  };

  return {
    getRecordings,
    analyzeAudio,
    getRecordingAudio,
    delete: deleteRecording,
    get,
  };
}; 