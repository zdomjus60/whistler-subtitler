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

Run the script from your terminal, providing the path to your video file and the desired output SRT file, along with optional parameters for language and model.

```bash
python whisper_subtitler.py <video_path> <srt_path> [--language <lang_code>] [--model <model_name>]
```

**Arguments:**

*   `<video_path>`: **Required.** Path to the input video file (e.g., `my_video.mp4`).
*   `<srt_path>`: **Required.** Path to the output SRT subtitle file (e.g., `my_video.srt`).
*   `--language <lang_code>`: Optional. Language of the audio in the video (e.g., `en` for English, `it` for Italian, `fr` for French). Default is `en`.
*   `--model <model_name>`: Optional. Faster-Whisper model to use (e.g., `tiny`, `base`, `small`, `medium`, `large`). Default is `small`.

**Examples:**

*   **Transcribe an English video to an English SRT:**
    ```bash
    python whisper_subtitler.py "path/to/your/video.mp4" "output.srt" --language en
    ```
*   **Transcribe an Italian video using the 'medium' model:**
    ```bash
    python whisper_subtitler.py "path/to/your/italian_video.mp4" "italian_output.srt" --language it --model medium
    ```

**Result:**

Upon completion, you will find the generated `.srt` file at the specified `srt_path`. The script will also take care of deleting the temporary audio file created during the process.

## How it Works

The script follows these steps:
1.  **Audio Extraction**: It uses `ffmpeg` to extract the audio track from the video file and temporarily save it as `audio.mp3`.
2.  **Transcription**: It loads the `small` model of `faster-whisper` (optimized for CPU) and transcribes the audio. It specifically requests word-level timestamps for greater accuracy.
3.  **SRT Formatting**: The text segments and their corresponding timestamps are formatted according to the SRT standard, grouping approximately 5 words per line for better readability.
4.  **Cleanup**: The temporary audio file (`audio.mp3`) is deleted at the end of the process.
