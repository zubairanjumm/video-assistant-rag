# AI Video Assistant — RAG

An AI-powered video and meeting assistant that turns long-form video or audio into structured, searchable knowledge.

It can process a **YouTube URL or local media file**, transcribe the content, generate a summary, extract important information, and let you **chat with the transcript using RAG**.

## Features

* 🎥 YouTube URL or local video/audio input
* 🎙️ Local speech-to-text using OpenAI Whisper
* 🌐 English and Hinglish transcription support
* 📝 Automatic transcript generation
* 📌 AI-generated session title
* 📋 Automatic summarisation
* ✅ Action-item extraction
* 🔑 Key-decision extraction
* ❓ Open-question extraction
* 🧠 Retrieval-Augmented Generation (RAG)
* 💬 Chat with the processed video/meeting
* 📦 Local ChromaDB vector store
* 🖥️ Streamlit web interface
* 💻 CLI interface

## How It Works

```text
YouTube URL / Local Video
          │
          ▼
   Audio Processing
          │
          ▼
   Whisper Transcription
          │
          ▼
      Transcript
          │
    ┌─────┼─────────────┐
    ▼     ▼             ▼
 Summary  Extraction   Title
    │     │
    │     ├── Action Items
    │     ├── Decisions
    │     └── Questions
    │
    ▼
  RAG Pipeline
    │
    ▼
 Vector Embeddings
    │
    ▼
   ChromaDB
    │
    ▼
 Question → Retrieval → LLM → Answer
```

## Tech Stack

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python                | Core application            |
| Streamlit             | Web UI                      |
| OpenAI Whisper        | Speech-to-text              |
| yt-dlp                | YouTube media acquisition   |
| FFmpeg                | Audio/video processing      |
| LangChain             | LLM/RAG orchestration       |
| Mistral               | LLM                         |
| Sentence Transformers | Text embeddings             |
| ChromaDB              | Vector database             |
| Hugging Face          | Embedding models            |
| Deep Translator       | Hindi → English translation |

## Project Structure

```text
video-assistant-rag/
│
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   └── transcriber.py
│
├── utils/
│   └── audio_processor.py
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/zubairanjumm/video-assistant-rag.git
cd video-assistant-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg must be installed separately because the project uses it for audio/video processing.

Make sure `ffmpeg` is available from your terminal:

```bash
ffmpeg -version
```

### 5. Configure environment variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

Do not commit your `.env` file to GitHub.

## Running the Application

### Streamlit UI

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

Enter either:

```text
https://youtube.com/watch?v=...
```

or a local media path:

```text
/path/to/video.mp4
```

Choose the language and click **Analyse**.

### CLI

You can also run the pipeline directly:

```bash
python main.py
```

The CLI will ask for:

```text
Enter YouTube URL or local file path:
Language (english/hinglish):
```

After processing, you can ask questions about the video directly from the terminal.

## RAG Pipeline

The RAG component converts the transcript into searchable chunks and creates embeddings using a Hugging Face/Sentence Transformers model.

The resulting embeddings are stored in **ChromaDB**.

When a question is asked:

```text
User Question
      ↓
Retriever
      ↓
Relevant Transcript Chunks
      ↓
Mistral LLM
      ↓
Context-aware Answer
```

This allows the assistant to answer questions based on the actual content of the processed video instead of relying only on the model's general knowledge.

## Example Questions

After processing a video or meeting, you can ask:

```text
What were the main decisions?

What action items were assigned?

What problems were discussed?

What did they say about the project timeline?

What are the unresolved questions?

Summarise the discussion about the technical architecture.
```

## Main Pipeline

The application processes the input through these stages:

1. **Audio Processing** — extracts/processes audio from the source.
2. **Transcription** — converts speech into text using Whisper.
3. **Title Generation** — generates a concise title from the transcript.
4. **Summarisation** — creates a summary of the content.
5. **Information Extraction** — identifies action items, decisions, and open questions.
6. **RAG Construction** — creates the retrieval pipeline for transcript-based Q&A.
7. **Conversational Q&A** — allows users to chat with the processed content.

## Use Cases

* Meeting analysis
* Lecture summarisation
* Educational video analysis
* YouTube research
* Interview analysis
* Technical discussion analysis
* Long-form video Q&A
* Personal knowledge extraction

## Current Limitations

* Whisper transcription can be computationally expensive locally.
* Video/audio processing depends on FFmpeg.
* LLM functionality requires a Mistral API key.
* Processing time depends on video length and available hardware.
* The current vector store is local ChromaDB rather than a production vector database.

## License

This project is for learning and experimentation with AI, RAG, speech-to-text, and LLM application development.
