import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Recording } from '../types';
import { Radar } from 'react-chartjs-2';
import { useApi } from '../api';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface Props {
  recordings: Recording[];
  onAudioRequest: (filename: string) => Promise<Blob>;
  onRecordingsUpdate: (recordings: Recording[]) => void;
}

export const RecordingsList: React.FC<Props> = ({ 
  recordings = [],
  onAudioRequest, 
  onRecordingsUpdate 
}) => {
  const [audioUrls, setAudioUrls] = useState<{ [key: string]: string }>({});
  const [isDeleting, setIsDeleting] = useState<{ [key: string]: boolean }>({});
  const { token } = useAuth();
  const api = useApi();

  const formatDate = (timestamp: string) => {
    try {
      // Parse ISO timestamp and format it nicely
      const date = new Date(timestamp);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).format(date);
    } catch (error) {
      console.error('Error formatting date:', error);
      return 'Invalid Date';
    }
  };

  const parseModelResponse = (response: string | null) => {
    if (!response) return null;
    try {
      return JSON.parse(response);
    } catch (error) {
      return null;
    }
  };

  const fetchAudio = async (filename: string) => {
    try {
      const audioBlob = await onAudioRequest(filename);
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrls(prev => ({ ...prev, [filename]: audioUrl }));
    } catch (error) {
      console.error('Error fetching audio:', error);
    }
  };

  const getGradeData = (recording: Recording) => {
    return {
      labels: ['Pronunciation', 'Fluency', 'Coherence', 'Grammar', 'Vocabulary'],
      datasets: [
        {
          label: 'Grades',
          data: [
            recording.pronunciation_grade ? recording.pronunciation_grade * 100 : 0,
            recording.fluency_grade ? recording.fluency_grade * 100 : 0,
            recording.coherence_grade ? recording.coherence_grade * 100 : 0,
            recording.grammar_grade ? recording.grammar_grade * 100 : 0,
            recording.vocabulary_grade ? recording.vocabulary_grade * 100 : 0,
          ],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 2,
          fill: true,
        },
      ],
    };
  };

  const chartOptions = {
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 20,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  const handleDelete = async (recordingId: number) => {
    try {
      setIsDeleting(prev => ({ ...prev, [recordingId]: true }));
      const response = await fetch(`/api/recordings/${recordingId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Delete failed:', errorText);
        throw new Error('Failed to delete recording');
      }

      // Only update UI after successful deletion
      onRecordingsUpdate(recordings.filter(r => r.id !== recordingId));
    } catch (error) {
      console.error('Error deleting recording:', error);
    } finally {
      setIsDeleting(prev => ({ ...prev, [recordingId]: false }));
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Your Recordings</h2>
      {!recordings ? (
        <p className="text-gray-500">Loading recordings...</p>
      ) : recordings.length === 0 ? (
        <p className="text-gray-500">No recordings found</p>
      ) : (
        <ul className="space-y-6">
          {recordings.map((recording) => {
            const modelResponse = parseModelResponse(recording.model_response);
            if (!audioUrls[recording.filename]) {
              fetchAudio(recording.filename);
            }
            return (
              <li key={recording.id} className="border rounded-lg p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-gray-600">Recorded at: </span>
                    <span className="font-medium">{formatDate(recording.timestamp)}</span>
                  </div>
                  <button
                    onClick={() => handleDelete(recording.id)}
                    disabled={isDeleting[recording.id]}
                    className="text-red-600 hover:text-red-800 disabled:opacity-50"
                  >
                    {isDeleting[recording.id] ? 'Deleting...' : 'Delete'}
                  </button>
                </div>
                
                {/* Audio Playback */}
                {audioUrls[recording.filename] && (
                  <div className="mb-4">
                    <audio 
                      controls 
                      src={audioUrls[recording.filename]}
                      className="w-full"
                    >
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                )}

                {recording.transcription && (
                  <div className="mb-4">
                    <span className="text-gray-600">Transcription: </span>
                    <span className="font-medium">{recording.transcription}</span>
                  </div>
                )}

                {/* Star Graph */}
                {(recording.pronunciation_grade || recording.fluency_grade || 
                  recording.coherence_grade || recording.grammar_grade || 
                  recording.vocabulary_grade) && (
                  <div className="mt-4">
                    <h4 className="font-medium mb-2">Performance Analysis</h4>
                    <div className="w-full max-w-md mx-auto h-64">
                      <Radar data={getGradeData(recording)} options={chartOptions} />
                    </div>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}; 