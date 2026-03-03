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

3. Install prerequisites with Homebrew. 
This project depends on FFmpeg 7 (not FFmpeg 8).
Newer versions of FFmpeg are not compatible with PyAV 14.x.
Inside your terminal window, run:  
```bash
   brew install git  
   brew install uv  
   brew install python  
   brew install ollama
   brew install ffmpeg@7
   brew install pkg-config
   brew install cython  
```

If you previously installed FFmpeg 8, remove it and use version 7.
```bash
brew uninstall ffmpeg
brew link ffmpeg@7 --force --overwrite
```

Install Xcode Command Line Tools (Required for C compilation)
```bash
xcode-select --install
```
If it says already installed, you are good.

4. PyAV requires pkg-config to locate FFmpeg libraries.
```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig"
echo 'export PKG_CONFIG_PATH="/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig"' >> ~/.zshrc
source ~/.zshrc
```


5. Clone this repository. Inside your terminal window, run:  
```bash
   git clone https://github.com/althearao/local-voice-ai-agent.git  
   cd local-voice-ai-agent  
```

6. Set up Python environment and install dependencies. Inside your terminal window, run:  
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

4. Restart Powershell. Then, clone this repository. Inside your PowerShell window, run:  
```bash
   git clone https://github.com/althearao/local-voice-ai-agent.git  
   cd local-voice-ai-agent  
```

5. Set up Python environment and install dependencies. Inside your PowerShell window, run:  
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
  Open PowerShell, navigate to the project folder, activate your virtual environment, run the script.
```bash
  cd local-voice-ai-agent #navigate to the project folder (you can also drag and drop)
  .venv\Scripts\activate #activate your virtual environment
  python text_to_voice.py
```
Once running:
	
-  Type your input into the terminal/PowerShell window
-	The text is sent to your Ollama model	
-  The response is printed as text and spoken aloud using Kokoro TTS	
-  Press Enter on a blank line to exit the program


## Using a different voice for chatbot

To use a different voice, uncomment the options variable in `text_to_voice.py` and pass it to the `stream_tts_sync` method like shown below:

```python
for sample_rate, audio_array in tts_model.stream_tts_sync(response_text, options=options):
```

You can check out all supported voices at:
[Supported Voices](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) and update the voice attribute in the options accordingly.

### Example for using af_nicole voice
```python
options = KokoroTTSOptions(
    voice="af_nicole",
    speed=1,
    lang="en-us"
)
```

Speed attribute controls how fast or slow the voice speaks. Higher the value, faster the pace of speech.

### Example for using a different accent
E.g: For Spanish accent, select one of the Spanish voices from the supported voices page and pass the corresponding `voice` and `lang` attribute:
```python
options = KokoroTTSOptions(
    voice="ef_dora",
    speed=1,
    lang="es"
)
```

Kokoro has not been trained much on other accents, so you might notice that other accents are spoken in a weird manner.

# Using Speech to Text for Input

In addition to typing input, this project also supports speech input using Moonshine Speech-to-Text (STT).

The following scripts support microphone input:

`moonshine_text_to_voice.py`


### Setup (Kokoro Environment)

Activate the default environment:

```python
source .venv/bin/activate        # macOS
```
OR

```python
.venv\Scripts\activate           # Windows
```

Installed STT dependencies:

```python
pip install "fastrtc[stt]"
```

Run the script
```python
python moonsine-text-to-voice.py
```


## Usage

Press Enter to start recording.

Speak into your microphone.

Press Enter again to stop recording.

Moonshine converts your speech to text.

The text is sent to your local Ollama model and the out is spoken back using Kokoro.


## Custom Voice Setup with Coqui

### Step 1: Create the Custom Voice Environment

Deactivate any active environment first:

```bash
deactivate
```

Create a new virtual environment:

### Why a Separate Environment?

The custom voice system depends on specific versions of:

- `torch`
- `transformers`
- `numpy`

These versions conflict with the default Kokoro setup.

To avoid dependency conflicts, custom voice runs inside `.venv_coqui`, while the standard Kokoro version runs inside `.venv`.

Both virtual environments are gitignored and must be created locally.

```bash
python3.11 -m venv .venv_coqui
```

Activate it:

**On macOS:**
```bash
source .venv_coqui/bin/activate
```

**On Windows:**
```bash
.venv_coqui\Scripts\activate
```

### Step 2: Install Required Dependencies

Inside the activated `.venv_coqui`, run:

```bash
pip install --upgrade pip
pip install "fastrtc[stt]"
pip install TTS
pip install torch==2.3.1 torchaudio==2.3.1
pip install transformers==4.40.2
pip install sounddevice ollama numpy
```

These packages are required for:

- Moonshine speech-to-text
- Coqui XTTS voice cloning
- Local audio playback

### Step 3: Add a Reference Voice File

Open `custom_voice_moonshine_text_to_voice.py` and set:

```python
REFERENCE_AUDIO = "your_voice.wav"
```

Place your WAV file in the project folder.
You can using online mp3 to wav converters.

### Step 4: Run the Custom Voice Version

Make sure you are in `.venv_coqui` virtual environment, then run:

```bash
python custom_voice_moonshine_text_to_voice.py
```

**Usage:**

- Press Enter to start recording
- Speak into your microphone
- Press Enter to stop recording
- Moonshine converts speech to text
- Ollama generates a response
- XTTS synthesizes speech using your reference voice
- Audio is played through your speakers




## How it works

The application uses:

- `Kokoro` for text-to-speech synthesis in kokoro version
- `Coqui` for text-to-speech synthesis using custom voice
- `Moonshine` from FastRTC for speech-to-text
- `Ollama` for running local LLM inference with your fine tuned models
- sounddevice for audio playback

