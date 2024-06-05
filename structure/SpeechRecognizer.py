import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class SpeechRecognizer():
    def __init__(self) -> None:
        MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-polish"

        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
    
    def transcribe_audio(self, filename):
        speech_array, sampling_rate = librosa.load(filename, sr=16000)
        
        inputs = self.processor(speech_array, sampling_rate=16000, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits
        
        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentence = self.processor.batch_decode(predicted_ids)
        
        return predicted_sentence[0]
