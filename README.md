# Video to SRT Transcription Script with Faster-Whisper

This Python script automates the process of extracting audio from a video file, transcribing it into text, and creating a subtitle file in SRT (`.srt`) format with precise word-level timestamps.

It uses `ffmpeg` for audio/video processing and `faster-whisper` for efficient, CPU-optimized transcription.

## Prerequisites

Before running the script, make sure you have the following software installed:

1.  **Python 3**: If not already installed, download it from the [official website](https://www.python.org/).
2.  **FFmpeg**: This is a crucial component for audio extraction.
    *   On Debian/Ubuntu-based systems, you can install it with the following command:
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```

## Installation

1.  **Create a virtual environment** (recommended to isolate project dependencies):
    ```bash
    python3 -m venv whisper-env
    source whisper-env/bin/activate
    ```

2.  **Install the necessary Python libraries**: The main dependency is `faster-whisper`. `pip` will automatically handle all other required libraries.
    ```bash
    pip install faster-whisper
    ```

## Usage Guide

1.  **Place the video file**: Put the video file you want to transcribe (e.g., `my_video.mp4`) in the same directory as the `whisper_subtitler.py` script.

2.  **Configure the script**: Open the `whisper_subtitler.py` file with a text editor and modify the following lines at the end of the file to specify the names of your input and output files:
    ```python
    if __name__ == "__main__":
        # Edit the name of your video file here
        video_path = 'The Most.mp4'  
        
        # Edit the name of the SRT file that will be generated here
        srt_path = 'The Most.srt'    
        
        # ... rest of the script ...
    ```

3.  **Run the script**: Launch the script from your terminal.
    ```bash
    python whisper_subtitler.py
    ```

4.  **Result**: Upon completion, you will find a new `.srt` file (e.g., `The Most.srt`) in the directory, ready to be used with your video. The script will also take care of deleting the temporary audio file created during the process.

## How it Works

The script follows these steps:
1.  **Audio Extraction**: It uses `ffmpeg` to extract the audio track from the video file and temporarily save it as `audio.mp3`.
2.  **Transcription**: It loads the `small` model of `faster-whisper` (optimized for CPU) and transcribes the audio. It specifically requests word-level timestamps for greater accuracy.
3.  **SRT Formatting**: The text segments and their corresponding timestamps are formatted according to the SRT standard, grouping approximately 5 words per line for better readability.
4.  **Cleanup**: The temporary audio file (`audio.mp3`) is deleted at the end of the process.