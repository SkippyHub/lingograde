const API_BASE = 'http://localhost:8000/api';

export const analyzeAudio = async (formData: FormData) => {
  const response = await fetch(`${API_BASE}/analyze-audio`, {
    method: 'POST',
    body: formData,
  });
  return response.json();
};

export const getRecordings = async () => {
  const response = await fetch(`${API_BASE}/recordings`);
  return response.json();
}; 