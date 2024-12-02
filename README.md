# lingograde
lingo grade, grades your speech, identifies issues, and enhances language skills to become a native speaker.

## Quick Start

### Development Setup

1. Using Docker (Recommended):
```bash
# Build development image
make docker-build-dev

# Run development environment
make docker-run-dev
```
This will start:
- Frontend dev server at http://localhost:3000
- Backend API at http://localhost:8000

2. Local Development:
```bash
# Install dependencies
make install

# Run development servers
make run
```

### Production Setup

1. Using Docker:
```bash
# Build production image
make docker-build

# Run production environment
make docker-run
```
This will start:
- Frontend at http://localhost
- Backend API at http://localhost:8000

## Architecture

### Component Overview
```mermaid
graph TD
A[main.py] --> B[model/predictor.py]
A --> C[database/db_manager.py]
A --> D[storage/storage_manager.py]
B --> E[AI Model Interface]
C --> F[(SQLite Database)]
D --> G[/storage/recordings/]
classDef main fill:#f96,stroke:#333,stroke-width:2px;
classDef component fill:#bbf,stroke:#333,stroke-width:2px;
classDef storage fill:#bfb,stroke:#333,stroke-width:2px;

class A main;
class B,C,D component;
class F,G storage;
```

### Data Flow Sequence
```mermaid
sequenceDiagram
    participant U as User
    participant M as Main App
    participant S as StorageManager
    participant D as DatabaseManager
    participant A as AIModel

    U->>M: Start Recording
    M->>M: Record Audio
    
    U->>M: Stop Recording
    M->>S: Save Audio File
    S-->>M: File Path
    
    M->>A: Process Audio
    A-->>M: Model Results
    
    M->>D: Save Recording Data
    D-->>M: Recording ID
    
    M->>D: Get Recordings
    D-->>M: Recording List
    M->>S: Get Audio Files
    S-->>M: Audio Files
    M->>U: Display Results
```

### File Structure and Responsibilities

1. **main.py**
   - Main Streamlit application entry point
   - Handles user interface and interaction
   - Coordinates between model, storage, and database components
   - Manages audio recording and playback

2. **model/predictor.py**
   - Contains the AIModel class
   - Handles speech processing and analysis
   - Returns predictions and transcriptions
   - Processes audio data into meaningful results

3. **database/db_manager.py**
   - Manages SQLite database operations
   - Stores recording metadata and results
   - Handles user sessions and recording history
   - Provides CRUD operations for recordings

4. **storage/storage_manager.py**
   - Manages physical file storage
   - Organizes recordings by user ID
   - Handles file saving and retrieval
   - Maintains directory structure

5. **storage/recordings/**
   - Physical storage location for audio files
   - Organized in user-specific directories
   - Contains WAV format audio recordings

### Data Flow
1. User records audio through Streamlit interface
2. Audio is saved via StorageManager
3. Audio is processed by AIModel
4. Results are stored in database via DatabaseManager
5. Results and audio playback are displayed in UI

## Features
### Recording
- Record from microphone
- Record from file
- Record from youtube

### Grading Skills 
Grades in a star graph, provide a prompt to read and analyze your speech.
It will grade your speech and provide a star graph with the grade.
A gauge on the certification level you are at.

#### Speech
- **Pronunciation**: How well you pronounce the words
- **Fluency**: How well you speak fluent, your melody is 
- **Coherence**: How well you speak coherent, your ideas are clear
- **Grammar**: How well you speak grammatically correct
- **Vocabulary**: How diverse your vocabulary is

#### Certification
- **CEFR scale grade**: A scale grade of your English level according to the CEFR scale (A1, A2, B1, B2, C1, C2)
- **IELTS scale grade**: A scale grade of your English level according to the IELTS scale (1-9)

## Goals MVP Challenge
### MVP 1
- Record from microphone
- Grading skills
- Star graph

### MVP 2
- Certification

## Stack
- Python
- Docker
- Streamlit
- Gemma

## Packages
- whisper (audio to text)
- gemma 2 (text to text)
- langchain (chaining models)
- dotenv (env variables)
- ffmpeg (audio processing)
- numpy (audio processing)
- pandas (audio processing)

## Additional Packages
- librosa (advanced audio analysis)
- pyDictionary (vocabulary enhancement)
- spaCy (NLP processing)
- pytest (testing framework)

## Installation

### Option 1: Local Installation
1. Prerequisites:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install pyenv
brew install ffmpeg
brew install pkg-config  # Required for audio processing
brew install portaudio   # Required for audio recording

# Add pyenv to your shell (for zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Install Python 3.11.7
pyenv install 3.11.7

# Set local Python version
pyenv local 3.11.7
```

2. Clone and setup:
```bash
# Clone repository
git clone https://github.com/skippyhub/lingograde.git
cd lingograde

# Install dependencies
make install
```

### Option 2: Using Docker
```bash
# Install Docker (macOS)
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Build and run
docker build -t lingograde .
docker run -p 8501:8501 lingograde
```

## Usage

### Local Usage
1. Run the application:
```bash
make run
```

2. Run tests:
```bash
make test
```

3. Format code:
```bash
make lint
```

4. Clean up:
```bash
make clean
```

### Docker Usage
```bash
# Run existing container
docker start lingograde

# Stop container
docker stop lingograde

# View logs
docker logs lingograde

# Rebuild after changes
docker build -t lingograde .
docker run -p 8501:8501 lingograde
```

Access the application at http://localhost:8501

## Development

### Docker Development Environment

The development environment uses:
- Hot reloading for both frontend and backend
- Volume mounting for live code updates
- Python 3.11 with Poetry for dependency management
- Node.js 18 with npm for frontend development
- Vite for frontend development server

### Environment Variables

Development environment variables are set in:
- `.env` for backend
- `frontend/.env` for frontend

Required environment variables:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=your-region
```

### Available Make Commands

use make and install, you need 

```bash
# Development (experimental)
make docker-build-dev    # Build development Docker image
make docker-run-dev      # Run development environment with hot reload
make docker-build       # Build production Docker image
make docker-run        # Run production environment

# Local Development Commands
make install           # Install dependencies
make run              # Run development servers locally
make frontend-dev     # Run frontend development server
make api              # Run API development server

# Utility Commands
make clean            # Clean build artifacts
make clean-all
make lint             # Run linters
make test             # Run tests
```

## Deployment

### Docker
```bash
docker build -t lingograde .
docker run -p 8501:8501 lingograde
```

### Google Cloud Setup

1. **Create a Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Note your `PROJECT_ID` and `REGION`

2. **Enable Required APIs**:
   ```bash
   # Enable Speech-to-Text API
   gcloud services enable speech.googleapis.com
   
   # Enable Cloud Run (if using deployment)
   gcloud services enable run.googleapis.com
   ```

3. **Set up Service Account**:
   - Go to IAM & Admin > Service Accounts
   - Create a new service account
   - Add roles:
     - `Speech-to-Text User`
     - `Cloud Run Admin` (for deployment)
   - Create and download JSON key
   - Rename and move the key:
   ```bash
   mv downloaded-key.json lingograde-stt-credentials.json
   ```

4. **Configure Environment**:
   ```bash
   # Add to your .env file
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_REGION=your-region
   
   # For local development
   GOOGLE_APPLICATION_CREDENTIALS=./lingograde-stt-credentials.json
   ```

5. **For GitHub Actions Deployment**:
   - Go to your GitHub repository settings
   - Add these secrets:
     - `GCP_SA_KEY`: Content of your service account JSON key
     - `GOOGLE_CLOUD_PROJECT`: Your project ID
     - `GOOGLE_CLOUD_REGION`: Your chosen region

Note: Keep your service account credentials secure and never commit them to version control.


