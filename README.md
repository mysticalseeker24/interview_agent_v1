# InterviewPilot.AI 🎯

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Anthropic Claude](https://img.shields.io/badge/AI-Claude%204%20Sonnet%20%26%20Opus-green.svg)](https://www.anthropic.com/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20Whisper%20%26%20TTS-orange.svg)](https://openai.com/)

> **Award-winning AI-powered interview practice system** - Winner of Anthropic's Build with Claude Competition

## 🚀 Overview

InterviewPilot.AI is a sophisticated, AI-powered interview preparation system that creates realistic, interactive practice experiences tailored to your specific role and background. Unlike static practice tools, our system provides dynamic, conversational interviews with intelligent follow-ups that adapt to your responses in real-time.

### ✨ Key Features

- **🎭 Multiple AI Personas**: Practice with 6 distinct interviewer personalities (Networker, Analyst, Listener, Planner, Storyteller, Data-Driven)
- **🗣️ Voice-to-Voice Interaction**: Complete speech-to-text-to-speech pipeline for natural conversation flow
- **📄 Document Intelligence**: Automatically processes resumes and job descriptions to generate personalized questions
- **🎚️ Adaptive Difficulty**: Choose from Easy, Medium, or Hard interview modes
- **📊 Performance Analytics**: Detailed feedback and evaluation based on predefined criteria
- **🔄 Real-time Processing**: Intelligent conversation management with context awareness

## 🏗️ Architecture

### Core Components

1. **Persona Generation Pipeline** (`persona-generation/`)
   - Base persona creation and job-specific fusion
   - Automated question generation from documents
   - Response evaluation criteria definition

2. **Conversational Interview Engine** (`conversational-dialog/`)
   - Real-time voice processing and transcription
   - AI-powered conversation management
   - Session recording and analysis

### Technology Stack

- **AI Models**: Anthropic Claude 4 (Sonnet & Opus) + OpenAI Whisper & TTS
- **Audio Processing**: PyAudio, Pygame for real-time interaction
- **Document Processing**: PyPDF2 for resume/job description parsing
- **Data Management**: Pandas, JSON for structured data handling

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Microphone**: Required for voice input
- **Speakers/Headphones**: Required for audio output
- **API Keys**: OpenAI and Anthropic API access

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mysticalseeker24/interview_agent_v1.git
cd interview_agent_v1
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv interview_env

# Activate virtual environment
# On Windows:
interview_env\Scripts\activate
# On macOS/Linux:
source interview_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the `conversational-dialog/` directory:

```bash
cd conversational-dialog
touch .env  # On Windows: type nul > .env
```

Add your API keys to the `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Verify Installation

```bash
# Test basic functionality
python -c "import anthropic, openai, pyaudio, pygame; print('All dependencies installed successfully!')"
```

## 🎯 Usage Guide

### Quick Start

1. **Navigate to the conversational dialog directory:**
   ```bash
   cd conversational-dialog
   ```

2. **Run the interview system:**
   ```bash
   python interviewer.py
   ```

3. **Select difficulty level** when prompted (easy/medium/hard)

4. **Start speaking** when you see "Recording..." - the system will automatically detect when you stop talking

5. **End the interview** by saying "I am done" or similar termination phrases

### Advanced Usage

#### Custom Persona Generation

1. **Add job descriptions** to `persona-generation/job-descriptions/`
2. **Add resumes** to `persona-generation/resumes/`
3. **Run the persona generation pipeline:**
   ```bash
   cd persona-generation
   python utils.py
   ```

#### Interview Analysis

After completing an interview, analyze your performance:

```bash
cd conversational-dialog
python summary.py
```

This generates a detailed report with:
- Interview transcript
- Response quality ratings
- Improvement recommendations

## ⚙️ Configuration

### Audio Settings

Modify audio parameters in `conversational-dialog/audioToText.py`:

```python
class AudioRecorder:
    def __init__(self,
                 format=pyaudio.paInt16,     # Audio format
                 channels=1,                  # Mono audio
                 rate=8000,                  # Sample rate
                 chunk_size=256,             # Buffer size
                 silence_threshold=300,       # Silence detection
                 silence_duration=5):        # Silence timeout
```

### Interview Personas

Available interviewer personas:

- **Emma** - The Enthusiastic Networker
- **Liam** - The Methodical Analyst
- **Olivia** - The Empathetic Listener
- **Ethan** - The Strategic Planner
- **Sophia** - The Creative Storyteller
- **Noah** - The Data-Driven Decider

## 🔧 API Requirements

### OpenAI API

- **Models Used**: `whisper-1` (transcription), `tts-1` (text-to-speech)
- **Rate Limits**: Standard OpenAI rate limits apply
- **Costs**: ~$0.006 per minute of audio transcription, ~$0.015 per 1K characters for TTS

### Anthropic API

- **Models Used**: `claude-sonnet-4-20250514` (main), `claude-opus-4-20250514` (persona generation)
- **Rate Limits**: Standard Anthropic rate limits apply
- **Costs**: ~$3 per million input tokens, ~$15 per million output tokens

## 🐛 Troubleshooting

### Common Issues

#### Audio Not Working
```bash
# Check microphone permissions
# Windows: Settings > Privacy > Microphone
# macOS: System Preferences > Security & Privacy > Microphone
# Linux: Check ALSA/PulseAudio configuration
```

#### File Permission Errors (Windows)
If you encounter `PermissionError: [WinError 32]` when running interviews:
```bash
# This is automatically handled by the improved file management system
# The system now includes:
# - Retry mechanism for file operations
# - Automatic cleanup of temporary files
# - Better error handling for Windows file locking
```

#### PyAudio Installation Issues
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux (Ubuntu/Debian)
sudo apt-get install python3-pyaudio
```

#### API Key Errors
- Verify API keys are correctly set in `.env` file
- Check API key permissions and quotas
- Ensure no extra spaces or quotes around keys

#### Import Errors
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Debug Mode

Enable verbose logging by modifying the interviewer script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with proper documentation
4. Add tests for new functionality
5. Submit a pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include type hints where appropriate

### Testing

Before submitting:

```bash
# Run basic functionality tests
python -m pytest tests/ -v

# Test audio functionality
python conversational-dialog/test-files/testing-initial-tts.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

**Original Development Team** (HackRU 2024):
- Jinal Shah
- Tej Shah
- Akash Shah
- Hirsh Ramani

**Current Maintainer**: Saksham Mishra

**Special Thanks**:
- Anthropic for Claude 4 Sonnet & Opus APIs
- OpenAI for Whisper and TTS APIs
- The open-source community for supporting libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/mysticalseeker24/interview_agent_v1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mysticalseeker24/interview_agent_v1/discussions)
- **Email**: Support requests via GitHub issues preferred

---

**⭐ If this project helps you ace your interviews, please give it a star!**
