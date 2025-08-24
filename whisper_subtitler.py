# Import necessary libraries. Replace `whisper` with `faster_whisper`
import time
from faster_whisper import WhisperModel
from datetime import timedelta
import subprocess
import os


def extract_audio(video_path, audio_path):
    print("Starting audio extraction...")
    command = [
        'ffmpeg',
        '-i',
        video_path,
        '-q:a',
        '0',
        '-map',
        'a',
        audio_path
    ]
    subprocess.run(command, check=True)
    print(f"Audio extraction completed. Audio file saved to: {audio_path}")

def format_timestamp(seconds):
    """Formats seconds into SRT timestamp format (HH:MM:SS,ms)."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def transcribe_audio(audio_path, language='en', model_name='small'):
    print("Starting audio transcription with word-level timestamps...")
    try:
        # --- CRUCIAL CHANGE FOR FASTER-WHISPER ---
        # Replace OpenAI Whisper model loading
        # with faster-whisper. We use device="cpu" and
        # compute_type="int8" to leverage Intel optimizations.
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        
        print("Faster-whisper model loaded and optimized.")
        
        
        segments, info = model.transcribe(audio_path, language=language, beam_size=5, word_timestamps=True)
        
        print("Transcription completed with word-level timestamps.")
        
        
        return segments
    except Exception as e:
        print(f"Error during transcription: {e}")
        return []

def write_srt(segments, srt_path):
    print("Starting SRT file writing with word-level timestamps...")
    
    
    with open(srt_path, 'w') as srt_file:
        segment_idx = 1
        
        # `segments` è un generatore, quindi lo iteriamo
        for segment in segments:
            
            if not segment.words:
                continue

            current_line_words = []
            current_line_start = None
            current_line_end = None

            
            for i, word_info in enumerate(segment.words):
                word_text = word_info.word.strip()
                if not word_text:
                    continue

                if current_line_start is None:
                    current_line_start = word_info.start

                current_line_words.append(word_text)
                current_line_end = word_info.end

                
                if len(current_line_words) >= 5 or i == len(segment.words) - 1:
                    srt_file.write(f"{segment_idx}\n")
                    srt_file.write(f"{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n")
                    srt_file.write(f"{ ' '.join(current_line_words)}\n\n")
                    segment_idx += 1
                    current_line_words = []
                    current_line_start = None
                    current_line_end = None

    print(f"SRT file written to {srt_path}.")

def main(video_path, srt_path, audio_path='audio.mp3'):
    extract_audio(video_path, audio_path)
    segments = transcribe_audio(audio_path, language='en')
    if segments:
        write_srt(segments, srt_path)
    else:
        print("No text segments found. Check audio or transcription parameters.")
    os.remove(audio_path)
    print("Cleanup completed.")

if __name__ == "__main__":
    video_path = 'The Most.mp4'
    srt_path = 'The Most.srt'
    print("--- Starting transcription process ---")
    start_time = time.time()  # <--- Registra il tempo di inizio

    main(video_path, srt_path)
    end_time = time.time()    # <--- Registra il tempo di fine
    duration = end_time - start_time
    print(f"--- Process completed in {duration:.2f} seconds ---")

