# lingograde
lingo grade, grades your speech, identifies issues, and enhances language skills to become a native speaker.

#features
#recording
- record from microphone
- record from file
- record from youtube

##grading skills 
grades in a star graph, provide a prompt to read and analyze your speech.
it will grade your speech and provide a star graph with the grade.
a gauge on the certification level you are at.

###speech
- pronunciation 
how well you pronounce the words
- fluency
how well you speak fluent, your melody is 
- Coherence
how well you speak coherent, your ideas are clear. 
- grammar
how well you speak grammatically correct.
- vocabulary 
how diverse your vocabulary is.

###certification
- CEFR scale grade.
a scale grade of your english level. according to the CEFR scale. 
A1, A2, B1, B2, C1, C2
- IELTS scale grade.
a scale grade of your english level. according to the IELTS scale. from 1 to 9.


##goals MVP challenge
### MVP 1
- record from microphone
- grading skills
- star graph

### MVP 2
- certification

##stack
- python
- docker
- streamlit
- gemma  

##packages
- whisper (audio to text)
- gemma 2 (text to text)
- langchain (chaining models)
- dotenv (env variables)
- ffmpeg (audio processing)
- numpy (audio processing)
- pandas (audio processing)


##Additional Packages
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Deployment

### Docker
```bash
docker build -t lingograde .
docker run -p 8501:8501 lingograde
```



