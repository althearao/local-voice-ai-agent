## Installation Instructions (macOS and Windows)

### macOS

1. Open Terminal  
   - Press Command + Space, type "Terminal", and press Enter.  
   - You should see something like:  
```bash
     your-mac:~ yourname$
```

2. Install Homebrew (if you don’t have it already). Inside your terminal window, run:  
```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. Install prerequisites with Homebrew. Inside your terminal window, run:  
```bash
   brew install git  
   brew install uv  
   brew install python  
   brew install ollama  
```

4. Clone this repository. Inside your terminal window, run:  
```bash
   git clone https://github.com/althearao/local-voice-ai-agent.git  
   cd local-voice-ai-agent  
```

5. Set up Python environment and install dependencies. Inside your terminal window, run:  
```bash
   uv venv  
   source .venv/bin/activate  
   uv sync  
```

---

### Windows

1. Open PowerShell  
   - Press Win + S, type "PowerShell", and press Enter.  
   - You should see something like:  
```bash
     PS C:\Users\YourName>
```

2. Install prerequisites (download from these URLs and install manually):  
   Git for Windows: https://git-scm.com/download/win  
   uv installer: https://github.com/astral-sh/uv/releases  
   Python for Windows: https://www.python.org/downloads/windows/  
   (during installation make sure to check "Add Python to PATH")  
   Ollama for Windows: https://ollama.ai/download  

3. Clone this repository. Inside your PowerShell window, run:  
```bash
   git clone https://github.com/althearao/local-voice-ai-agent.git  
   cd local-voice-ai-agent  
```

4. Set up Python environment and install dependencies. Inside your PowerShell window, run:  
```bash
   uv venv  
   .venv\Scripts\activate  
   uv sync  
```


### 5. Configure your model

Open text_to_voice.py and edit the code so it calls the name of your Ollama model (default is class_murmur).


## Usage

### text to voice chat

```bash
python text_to_voice.py
```

## How it works

The application uses:

- `Kokoro` for text-to-speech synthesis
- `Ollama` for running local LLM inference with your fine tuned models
- sounddevice for audio playback

Workflow:
	1.	You type input into the terminal
	2.	Input is sent to your local LLM via Ollama
	3.	The LLM response is converted to speech with Kokoro
	4.	The audio is played aloud through your speakers
