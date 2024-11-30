import React from 'react';

interface Props {
  recordings: any[];
  onRecordingSelect: (recording: any) => void;
}

export const RecordingsList: React.FC<Props> = ({ recordings, onRecordingSelect }) => {
  return (
    <div>
      <h2>Recordings</h2>
      {recordings.map((recording, index) => (
        <div 
          key={index}
          onClick={() => onRecordingSelect(recording)}
          style={{
            padding: '10px',
            margin: '5px 0',
            border: '1px solid #ddd',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          <div>Recording {index + 1}</div>
          <div>{new Date(recording.timestamp).toLocaleString()}</div>
        </div>
      ))}
    </div>
  );
}; 