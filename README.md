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
   Python for Windows: https://www.python.org/downloads/windows/  
   (during installation make sure to check "Add Python to PATH")  
   Ollama for Windows: https://ollama.ai/download  

3. Install UV
```bash
   # On Windows.
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Restart Powershell. Then, clone this repository. Inside your PowerShell window, run:  
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

## Run your Ollama model

You need to tell the program which Ollama model to use. Open a new Terminal / Powershell and type:

```bash
   ollama run mymodel
```
Edit mymodel so it matches the name of your chatbot.

If you do not yet have a local Ollama chatbot set up, please refer to this tutorial. https://sjsu.instructure.com/courses/1616480/modules/items/17062651

Once Ollama is running, leave the Terminal / Powershell window open in the background and continue to the next step.

## Configure your model

1. Open the `text_to_voice.py` file in VS Code.  
   - On macOS, from your terminal window:
     ```bash
     code text_to_voice.py
     ```
   - On Windows, from your PowerShell window:
     ```powershell
     code text_to_voice.py
     ```
   *(If `code` doesn’t work, open VS Code manually and drag the file into the editor.)*

2. Go to **line 20**, which looks like this:
   ```python
   response = chat(
       model="class_murmur",  # your local model
       messages=[{"role": "user", "content": user_input}]
   )

3. Replace "class_murmur" with the name of the Ollama model you want to use.

4.	Save the file before running the program.


## Usage

### Run the text-to-voice chat

- **On macOS**  
  Open a new **Terminal**:  
```bash
  cd local-voice-ai-agent #navigate to the project folder (you can also drag and drop)
  source .venv/bin/activate #activate your virtual environment
  python text_to_voice.py
```

- **On Windows**  
  Open PowerShell, navigate to the project folder, activate your virtual environment, then run:
```bash
  cd local-voice-ai-agent #navigate to the project folder (you can also drag and drop)
  .venv\Scripts\activate #activate your virtual environment
  python text_to_voice.py
```
Once running:
	
-   Type your input into the terminal/PowerShell window
-	The text is sent to your Ollama model	
-   The response is printed as text and spoken aloud using Kokoro TTS	
-   Press Enter on a blank line to exit the program


## How it works

The application uses:

- `Kokoro` for text-to-speech synthesis
- `Ollama` for running local LLM inference with your fine tuned models
- sounddevice for audio playback

Workflow:
	
-  You type input into the terminal	
-   Input is sent to your local LLM via Ollama	
-   The LLM response is converted to speech with Kokoro
-   The audio is played aloud through your speakers
