import React from 'react';

interface Props {
  transcription?: string;
  metadata?: {
    confidence: number;
    sentiment: string;
    audio_duration: number;
    timestamp: string;
  };
}

export const TranscriptionView: React.FC<Props> = ({ 
  transcription = 'No transcription available', 
  metadata 
}) => {
  const [isMetadataOpen, setIsMetadataOpen] = React.useState(false);

  const toggleMetadata = () => {
    setIsMetadataOpen(!isMetadataOpen);
  };

  return (
    <div className="transcription-view">
      <div className="transcription-section">
        <h3>Transcription</h3>
        <p>{transcription}</p>
      </div>
      
      <div className="metadata-section">
        <button 
          onClick={toggleMetadata}
          style={{
            background: 'none',
            border: '1px solid #ddd',
            padding: '8px 16px',
            borderRadius: '4px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            width: '100%',
            justifyContent: 'space-between'
          }}
        >
          <span>Metadata</span>
          <span>{isMetadataOpen ? '▼' : '▶'}</span>
        </button>
        
        {isMetadataOpen && metadata && (
          <div 
            style={{
              padding: '16px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              marginTop: '8px'
            }}
          >
            <div>Confidence: {(metadata.confidence * 100).toFixed(1)}%</div>
            <div>Sentiment: {metadata.sentiment}</div>
            <div>Duration: {metadata.audio_duration.toFixed(2)}s</div>
            <div>Recorded: {new Date(metadata.timestamp).toLocaleString()}</div>
          </div>
        )}
      </div>
    </div>
  );
}; 