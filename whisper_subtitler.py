# Importa le librerie necessarie. Sostituisci `whisper` con `faster_whisper`
import time
import argparse
from faster_whisper import WhisperModel
from datetime import timedelta
import subprocess
import os
# Non abbiamo bisogno di importare torch per controllare la disponibilità di CUDA
# dal momento che useremo un'altra logica.
# import torch

# Non serve più questa funzione, la logica di `faster-whisper` è diversa
# e non si basa sul check di CUDA. La gestione del dispositivo è implicita
# o specificata nella creazione del modello.
# def check_cuda_availability():
#     print("Verifica disponibilità CUDA...")
#     if torch.cuda.is_available():
#         print("CUDA è disponibile. Utilizzo della GPU.")
#         device = "cuda"
#     else:
#         print("CUDA non è disponibile. Utilizzo della CPU.")
#         device = "cpu"
#     return device

def extract_audio(video_path, audio_path):
    print("Inizio estrazione audio...")
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
    print(f"Estrazione audio completata. File audio salvato in: {audio_path}")

def format_timestamp(seconds):
    """Formats seconds into SRT timestamp format (HH:MM:SS,ms)."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def transcribe_audio(audio_path, language='en', model_name='small'):
    print("Inizio trascrizione audio con timestamp a livello di parola...")
    try:
        # --- MODIFICA CRUCIALE PER FASTER-WHISPER ---
        # Sostituisci il caricamento del modello di OpenAI Whisper
        # con quello di faster-whisper. Usiamo device="cpu" e
        # compute_type="int8" per sfruttare le ottimizzazioni Intel.
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        
        print("Modello faster-whisper caricato e ottimizzato.")
        
        # faster-whisper non ha bisogno di `options` e `transcribe_options`
        # in questo modo. L'API è più semplice.
        # word_timestamps è abilitato di default con un'opzione nel metodo transcribe.
        segments, info = model.transcribe(audio_path, language=language, beam_size=5, word_timestamps=True)
        
        print("Trascrizione completata con timestamp a livello di parola.")
        
        # faster-whisper restituisce un generatore, che è ciò che ci serve.
        # Lo ritorniamo direttamente.
        return segments
    except Exception as e:
        print(f"Errore durante la trascrizione: {e}")
        return []

def write_srt(segments, srt_path):
    print("Inizio scrittura file SRT con timestamp a livello di parola...")
    
    # faster-whisper restituisce i segmenti in modo leggermente diverso.
    # L'output è un generatore, quindi il tuo ciclo `for` funzionerà,
    # ma la struttura interna dei segmenti è diversa.
    # Adattiamo il codice di scrittura in base alla nuova struttura.
    with open(srt_path, 'w') as srt_file:
        segment_idx = 1
        
        # `segments` è un generatore, quindi lo iteriamo
        for segment in segments:
            # I segmenti di faster-whisper hanno direttamente l'attributo `words`
            if not segment.words:
                continue

            current_line_words = []
            current_line_start = None
            current_line_end = None

            # Qui iteriamo sugli oggetti `Word` di faster-whisper
            for i, word_info in enumerate(segment.words):
                word_text = word_info.word.strip()
                if not word_text:
                    continue

                if current_line_start is None:
                    current_line_start = word_info.start

                current_line_words.append(word_text)
                current_line_end = word_info.end

                # Il resto della tua logica per la scrittura delle righe rimane
                if len(current_line_words) >= 5 or i == len(segment.words) - 1:
                    srt_file.write(f"{segment_idx}\n")
                    srt_file.write(f"{format_timestamp(current_line_start)} --> {format_timestamp(current_line_end)}\n")
                    srt_file.write(f"{ ' '.join(current_line_words)}\n\n")
                    segment_idx += 1
                    current_line_words = []
                    current_line_start = None
                    current_line_end = None

    print(f"File SRT scritto in {srt_path}.")

def main(video_path, srt_path, language='en', model_name='small', audio_path='audio.mp3'):
    extract_audio(video_path, audio_path)
    segments = transcribe_audio(audio_path, language=language, model_name=model_name)
    if segments:
        write_srt(segments, srt_path)
    else:
        print("Nessun segmento di testo trovato. Verifica l'audio o i parametri di trascrizione.")
    os.remove(audio_path)
    print("Pulizia completata.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio from video and generate SRT subtitles.")
    parser.add_argument("video_path", type=str, help="Path to the input video file.")
    parser.add_argument("srt_path", type=str, help="Path to the output SRT subtitle file.")
    parser.add_argument("--language", type=str, default="en", help="Language of the audio (e.g., 'en', 'it', 'fr'). Default is 'en'.")
    parser.add_argument("--model", type=str, default="small", help="Whisper model to use (e.g., 'tiny', 'base', 'small', 'medium', 'large'). Default is 'small'.")

    args = parser.parse_args()

    print("--- Avvio del processo di trascrizione ---")
    start_time = time.time()  # <--- Registra il tempo di inizio

    main(args.video_path, args.srt_path, args.language, args.model)
    end_time = time.time()    # <--- Registra il tempo di fine
    duration = end_time - start_time
    print(f"--- Processo completato in {duration:.2f} secondi ---")

