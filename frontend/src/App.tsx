import React, { useState, useEffect } from 'react';
import { AudioRecorder } from './components/AudioRecorder';
import { GradesChart } from './components/GradesChart';
import { TranscriptionView } from './components/TranscriptionView';
import { RecordingsList } from './components/RecordingsList';
import { analyzeAudio, getRecordings } from './api';

const App: React.FC = () => {
  const [currentResult, setCurrentResult] = useState<any>(null);
  const [recordings, setRecordings] = useState<any[]>([]);

  useEffect(() => {
    loadRecordings();
  }, []);

  const loadRecordings = async () => {
    const data = await getRecordings();
    setRecordings(data);
  };

  const handleAudioRecorded = async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const result = await analyzeAudio(formData);
    setCurrentResult(result);
    await loadRecordings();
  };

  return (
    <div className="app">
      <header>
        <h1>LingoGrade</h1>
      </header>
      
      <main className="content">
        <div className="left-panel">
          <AudioRecorder onRecordingComplete={handleAudioRecorded} />
          
          {currentResult && (
            <div className="analysis-results">
              <TranscriptionView 
                transcription={currentResult.transcription}
                metadata={currentResult.metadata}
              />
            </div>
          )}
        </div>
        
        <div className="right-panel">
          {currentResult?.grades && (
            <GradesChart grades={currentResult.grades} />
          )}
        </div>
        
        <aside className="recordings-panel">
          <RecordingsList 
            recordings={recordings}
            onRecordingSelect={setCurrentResult}
          />
        </aside>
      </main>
    </div>
  );
};

export default App; 