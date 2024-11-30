import React from 'react';

interface Props {
  transcription: string;
  metadata: any;
}

export const TranscriptionView: React.FC<Props> = ({ transcription, metadata }) => {
  return (
    <div>
      <h3>Transcription</h3>
      <p>{transcription}</p>
      
      <h3>Metadata</h3>
      <pre>{JSON.stringify(metadata, null, 2)}</pre>
    </div>
  );
}; 