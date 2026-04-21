# 🎙️ Intelligent Voice Assistant

A modular, scalable, and intelligent Voice Assistant built with Python. It can understand voice commands, perform tasks, and provides a sleek GUI.

## ✨ Features
- **Speech-to-Text**: High-accuracy recognition using Google Speech Recognition.
- **Text-to-Speech**: Natural sounding offline voice output.
- **Intent Recognition**: Intelligent command parsing.
- **Task Automation**:
  - Open applications (Chrome, Notepad, Calculator, VS Code).
  - Web searching (Google, Wikipedia).
  - Weather information (via OpenWeatherMap API).
  - Time & Date announcements.
  - Basic calculations.
- **Wake Word Detection**: Activate the assistant with "Hey Assistant".
- **Modern GUI**: Sleek Dracular-themed interface with status indicators.

## 🛠️ Architecture
- `speech/`: Handles STT and TTS.
- `core/`: Intent logic and command execution.
- `gui/`: Tkinter-based visual interface.
- `config/`: System settings and environment management.

## 🚀 Getting Started

### 1. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file (or edit the template) to add your API keys:
- `OPENWEATHER_API_KEY`: Get one from [OpenWeatherMap](https://openweathermap.org/api).
- `NEWS_API_KEY`: Get one from [NewsAPI](https://newsapi.org/).
- `OPENAI_API_KEY`: Optional, for advanced AI responses.

### 3. Usage
Run in **CLI Mode**:
```bash
python main.py
```

Run in **GUI Mode**:
```bash
python main.py --gui
```

## ⌨️ Common Commands
- "Hey Assistant, what time is it?"
- "Hey Assistant, search for space exploration on Google."
- "Hey Assistant, who is Albert Einstein on Wikipedia?"
- "Hey Assistant, calculate 50 plus 25."
- "Hey Assistant, open chrome."
- "Hey Assistant, how is the weather?"

## 🧪 Advanced Features (Coming Soon)
- OpenAI GPT-4 Integration for complex conversations.
- Multi-language support.
- Voice authentication.
- IoT integration for smart home control.
