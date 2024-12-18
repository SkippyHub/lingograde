import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Recording } from '../types';
import { Radar } from 'react-chartjs-2';
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
    <div className="bg-white rounded-lg shadow px-6 pb-8 pt-8">
      <div className="relative">
        <div className="absolute -top-10 left-6">
          <div className="inline-flex items-center justify-center p-3 bg-indigo-500 rounded-md shadow-lg">
            <span className="h-6 w-6 text-white">📝</span>
          </div>
        </div>
        <h2 className="text-lg font-medium text-gray-900 tracking-tight pt-4">Your Recordings</h2>
        {!recordings ? (
          <p className="text-gray-500 mt-4">Loading recordings...</p>
        ) : recordings.length === 0 ? (
          <p className="text-gray-500 mt-4">No recordings found</p>
        ) : (
          <ul className="space-y-6 mt-6">
            {recordings.map((recording) => {
              if (!audioUrls[recording.filename]) {
                fetchAudio(recording.filename);
              }
              return (
                <li key={recording.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <span className="text-gray-600">Recorded at: </span>
                      <span className="font-medium text-gray-900">{formatDate(recording.timestamp)}</span>
                    </div>
                    <button
                      onClick={() => handleDelete(recording.id)}
                      disabled={isDeleting[recording.id]}
                      className="text-red-600 hover:text-red-700 disabled:opacity-50 transition-colors"
                    >
                      {isDeleting[recording.id] ? 'Deleting...' : 'Delete'}
                    </button>
                  </div>

                  {/* Star Graph - Moved to top */}
                  {(recording.pronunciation_grade || recording.fluency_grade || 
                    recording.coherence_grade || recording.grammar_grade || 
                    recording.vocabulary_grade) && (
                    <div className="mb-6">
                      <h4 className="font-medium text-gray-900 mb-4">Performance Analysis</h4>
                      <div className="flex justify-center">
                        <div className="w-64 h-64"> {/* Fixed size and centered */}
                          <Radar data={getGradeData(recording)} options={chartOptions} />
                        </div>
                      </div>
                    </div>
                  )}
                  
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

                  {/* Speech Content Section */}
                  <div className="space-y-4 mt-4">
                    {recording.transcription && (
                      <div className="space-y-4">
                        <div className="bg-indigo-50/50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-indigo-800 mb-2">Speaking Prompt:</h4>
                          <p className="text-indigo-900">{recording.prompt || "No prompt recorded"}</p>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-gray-700 mb-2">Your Speech:</h4>
                          <p className="text-gray-900">{recording.transcription}</p>
                        </div>
                      </div>
                    )}

                    {recording.model_response && (
                      <div className="bg-indigo-50 p-4 rounded-lg space-y-4">
                        <h4 className="text-sm font-medium text-indigo-800">AI Feedback:</h4>
                        {(() => {
                          try {
                            const response = JSON.parse(recording.model_response);
                            return (
                              <div className="space-y-4">
                                {/* Transcription */}
                                {response.transcription && (
                                  <div>
                                    <span className="text-xs font-medium text-indigo-700">Your Speech:</span>
                                    <p className="text-sm text-indigo-900 mt-1">{response.transcription}</p>
                                  </div>
                                )}

                                {/* Grading Details */}
                                {response.grading_details && (
                                  <div className="bg-white/50 p-3 rounded-md space-y-2">
                                    <span className="text-xs font-medium text-indigo-700">Detailed Analysis:</span>
                                    {recording.grading_explanation && (
                                      <p className="text-sm text-indigo-900">{recording.grading_explanation}</p>
                                    )}
                                    {recording.grading_notes && (
                                      <div className="mt-2">
                                        <span className="text-xs font-medium text-indigo-700">Additional Notes:</span>
                                        <p className="text-sm text-indigo-900 mt-1">{recording.grading_notes}</p>
                                      </div>
                                    )}
                                  </div>
                                )}

                                {/* Grades Visualization remains the same */}
                                <div className="mt-4">
                                  <span className="text-xs font-medium text-indigo-700">Performance Metrics:</span>
                                  <div className="grid grid-cols-2 gap-2 mt-2">
                                    {Object.entries({
                                      Pronunciation: recording.pronunciation_grade,
                                      Fluency: recording.fluency_grade,
                                      Coherence: recording.coherence_grade,
                                      Grammar: recording.grammar_grade,
                                      Vocabulary: recording.vocabulary_grade
                                    }).map(([key, value]) => (
                                      <div key={key} className="bg-white/50 p-2 rounded">
                                        <span className="text-xs text-indigo-700">{key}:</span>
                                        <div className="flex items-center">
                                          <div className="flex-grow bg-gray-200 h-2 rounded-full">
                                            <div 
                                              className="bg-indigo-600 h-2 rounded-full" 
                                              style={{ width: `${(value || 0) * 100}%` }}
                                            />
                                          </div>
                                          <span className="ml-2 text-xs text-indigo-900">
                                            {Math.round((value || 0) * 100)}%
                                          </span>
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                </div>

                                {/* AI Response */}
                                {response.response && (
                                  <div className="mt-4">
                                    <span className="text-xs font-medium text-indigo-700">AI Response:</span>
                                    {(() => {
                                      try {
                                        // Try to parse if response is a JSON string
                                        const parsedResponse = typeof response.response === 'string' && 
                                          response.response.startsWith('```json') ? 
                                          JSON.parse(response.response.replace(/```json|```/g, '').trim()) :
                                          { response: response.response };

                                        return (
                                          <div className="space-y-2">
                                            <p className="text-sm text-indigo-900 mt-1">
                                              {parsedResponse.response}
                                            </p>
                                            {parsedResponse.confidence && (
                                              <div className="text-xs text-indigo-600">
                                                Confidence: {Math.round(parsedResponse.confidence * 100)}%
                                              </div>
                                            )}
                                            {parsedResponse.sentiment && (
                                              <div className="text-xs text-indigo-600">
                                                Sentiment: {parsedResponse.sentiment}
                                              </div>
                                            )}
                                          </div>
                                        );
                                      } catch (e) {
                                        // Fallback to displaying raw response
                                        return <p className="text-sm text-indigo-900 mt-1">{response.response}</p>;
                                      }
                                    })()}
                                  </div>
                                )}
                              </div>
                            );
                          } catch (e) {
                            return <p className="text-sm text-indigo-900">{recording.model_response}</p>;
                          }
                        })()}
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
}; 