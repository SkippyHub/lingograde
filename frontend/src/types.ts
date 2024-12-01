export interface Recording {
  id: number;
  user_id: string;
  filename: string;
  timestamp: string;
  duration: number | null;
  transcription: string | null;
  model_response: string | null;
  metadata: string | null;
  prompt: string | null;
  pronunciation_grade: number | null;
  fluency_grade: number | null;
  coherence_grade: number | null;
  grammar_grade: number | null;
  vocabulary_grade: number | null;
  grading_explanation: string | null;
  grading_notes: string | null;
} 