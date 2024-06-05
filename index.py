from fastapi import FastAPI, File, UploadFile
import scipy.io.wavfile as wav
import sounddevice as sd
from fastapi.middleware.cors import CORSMiddleware
from structure.BEZIK import BEZIK
from structure.SpeechRecognizer import SpeechRecognizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = BEZIK(False)
speech_recognizer = SpeechRecognizer()

@app.get("/command/{req}")
def execute_command(req: str):
    operation = model(req.replace('%', ' '))

    return { "status": 200, "operation": operation, }

@app.get("/upload")
async def upload_file():
    duration = 7
    fs=16000

    print("Start speaking...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording finished.")
    wav.write("recording.wav", fs, recording)


@app.get("/read")
def read_item():
    transcription = speech_recognizer.transcribe_audio("recording.wav")
    operation = model(transcription.replace('%', ' '))

    return { "status": 200, "operation": operation, "transcription": transcription }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)