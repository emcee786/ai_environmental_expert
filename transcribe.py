import os
import pandas as pd
import tempfile
import whisper
from pytube import YouTube
from blob_storage import upload_txt_to_blob

DATA_PATH = "rag_data/txts"
os.makedirs(DATA_PATH, exist_ok=True)


def transcribe_youtube_video(YOUTUBE_VIDEO: str):
    youtube = YouTube(YOUTUBE_VIDEO)
    video_title = youtube.title
    save_as = video_title.lower().replace(" ", "-")
    video_url = youtube.watch_url
    
    
    TRANSCRIPTION_FILE = os.path.join(DATA_PATH, f"vid_{save_as}.txt")
    
    if not os.path.exists(TRANSCRIPTION_FILE):

        audio = youtube.streams.filter(only_audio=True).first()
        print(f"Processing video: {video_title}")
        

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
        
        upload_txt_to_blob(TRANSCRIPTION_FILE, f"vid_{save_as}.txt")
        


def transcribe_audio_file(audio:str, save_as: str):
    TRANSCRIPTION_FILE = os.path.join(DATA_PATH, f"{save_as}.txt")
 
    if not os.path.exists(TRANSCRIPTION_FILE):
        whisper_model = whisper.load_model("base")
        
        # Transcribe audio file
        transcription = whisper_model.transcribe(audio, fp16=False)["text"].strip()
       
        # Store the transcription in a string variable
        with open(TRANSCRIPTION_FILE, "w") as file:
            file.write(transcription)
    
    
def process_youtube_csv(csv_file: str):
    try:
        df = pd.read_csv(csv_file, delimiter=',', header=None, on_bad_lines='skip')
        for url in df[0]:
            transcribe_youtube_video(url)
    except pd.errors.ParserError as e:
        print(f"Error reading the CSV file: {e}")





# ## TEST CODE 
# video =  "https://youtu.be/tvHv3sguT3U"

            
# transcribe_youtube_video(video)


# audio = "data/voicenote.wav"
# audio_title = "voice-note"

# transcribe_audio_file(audio, audio_title)

# if __name__ == "__main__":
#     csv_file_path = "rag_data/youtube_links.csv"  
#     process_csv(csv_file_path)