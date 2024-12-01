import React, { useState } from 'react';

interface Props {
  onRecordingComplete: (blob: Blob) => void;
}

export const AudioRecorder: React.FC<Props> = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: BlobPart[] = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        onRecordingComplete(blob);
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <button 
      onClick={isRecording ? stopRecording : startRecording}
      className={`btn ${isRecording ? 'btn-secondary' : 'btn-primary'}`}
    >
      {isRecording ? 'Stop Recording' : 'Start Recording'}
    </button>
  );
}; 