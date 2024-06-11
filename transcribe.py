import os
import tempfile
import whisper
from pytube import YouTube


DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)


def transcribe_youtube_video(YOUTUBE_VIDEO: str, save_as: str):
    TRANSCRIPTION_FILE = os.path.join(DATA_PATH, f"{save_as}.txt")
   
    if not os.path.exists(TRANSCRIPTION_FILE):
        youtube = YouTube(YOUTUBE_VIDEO)
        video_title = youtube.title
        video_url = youtube.watch_url
        audio = youtube.streams.filter(only_audio=True).first()
        print("function got to here")
        

        whisper_model = whisper.load_model("base")
        
        # Transcribe the audio file
        with tempfile.TemporaryDirectory() as tmpdir:
            file = audio.download(output_path=tmpdir)
            transcription = whisper_model.transcribe(file, fp16=False)["text"].strip()

        # Save the transcription 
        with open(TRANSCRIPTION_FILE, "w") as file:
            file.write(f"Title: {video_title}\n")
            file.write(f"URL: {video_url}\n\n")
            file.write(transcription)


def transcribe_audio_file(audio:str, save_as: str):
    TRANSCRIPTION_FILE = os.path.join(DATA_PATH, f"{save_as}.txt")
 
    if not os.path.exists(TRANSCRIPTION_FILE):
        whisper_model = whisper.load_model("base")
        
        # Transcribe the audio file
        transcription = whisper_model.transcribe(audio, fp16=False)["text"].strip()
       
        # Store the transcription in a string variable
        with open(TRANSCRIPTION_FILE, "w") as file:
            file.write(transcription)
    
    


# ## TEST CODE 
# video =  "https://youtu.be/tvHv3sguT3U"
# video_title = "recycle-plastic2"
            
# transcribe_youtube_video(video, video_title)


# audio = "data/voicenote.wav"
# audio_title = "voice-note"

# transcribe_audio_file(audio, audio_title)

