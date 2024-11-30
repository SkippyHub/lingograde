# Contributing to LingoGrade

Thank you for your interest in contributing to LingoGrade! Here's how you can help.
w
## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/lingograde.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Option 1: Local Development

1. Install prerequisites:
```bash
# macOS Prerequisites

# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install pyenv
brew install ffmpeg
brew install pkg-config
brew install portaudio

# Configure shell for pyenv (for zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# For bash users, use ~/.bash_profile instead of ~/.zshrc

# Ubuntu/Debian Prerequisites
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev 
ffmpeg
```

2. Install Python:
```bash
# Install Python 3.11.7
pyenv install 3.11.7

# Set local version
pyenv local 3.11.7
```

3. Setup project:
```bash
# Install dependencies
make install

# Run tests
make test
```

### Option 2: Docker Development
```bash
# macOS Prerequisites
brew install --cask docker

# Build development container
docker build -t lingograde-dev -f Dockerfile.dev .

# Run with volume mount for live code changes
docker run -p 8501:8501 -v $(pwd):/app lingograde-dev

# Run tests in container
docker exec lingograde-dev make test

# Format code
docker exec lingograde-dev make lint
```

### Docker Tips
- Use `docker-compose up` for development with multiple services
- Hot-reload is enabled by default with volume mounting
- Database persists in Docker volume

## Making Changes

1. Make your changes in your feature branch
2. Follow the existing code style
3. Add tests if applicable
4. Update documentation as needed

## Commit Guidelines

- Use clear and meaningful commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep commits focused and atomic

Example:

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Ensure all tests pass
3. Create a Pull Request with a clear description of the changes
4. Link any related issues

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic

## Questions?

Feel free to open an issue for any questions or concerns.