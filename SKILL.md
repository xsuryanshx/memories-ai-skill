---
name: memories-ai
description: Video understanding and media processing using memories.ai API. Use for: (1) Uploading media files, (2) Video/image chat with Qwen VL models, (3) YouTube transcripts, (4) Text/image/video embeddings.
---

# Memories.ai Skill

Video understanding and media processing API using Qwen VL models.

## Status

**Working:** ✅ All core endpoints tested and working

## Setup

```bash
export MEMORIES_AI_API_KEY="your-api-key"
```

Get your API key at: https://memories.ai/api-key

## Working Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/upload` | POST (multipart) | ✅ Working | Upload files, returns asset_id |
| `/vu/chat/completions` | POST | ✅ Working | Use `qwen:qwen3-vl-plus` model |
| `/youtube/video/transcript` | POST | ✅ Working | Requires channel parameter |
| `/embeddings/text` | POST | ✅ Working | Use `input` array |
| `/embeddings/video` | POST | ✅ Working | Requires video asset_id |
| `/embeddings/image` | POST | ✅ Working | File or URL |

## Not Working (API Issues)

| Endpoint | Status | Issue |
|----------|--------|-------|
| `/list-videos` | ❌ | Request method not supported |
| `/search-memories` | ❌ | Request method not supported |
| `/delete` | ❌ | Request method not supported |

## Usage

### Text Chat

```python
from scripts.memories_client import MemoriesAIClient

client = MemoriesAIClient(api_key="your-key")

# Text-only chat
result = client.chat_text("Hello!")
print(result["choices"][0]["text"])
```

### Video/Image Chat

```python
# Chat with video
result = client.chat_with_video(
    video_url="https://example.com/video.mp4",
    prompt="What's in this video?"
)
print(result["choices"][0]["text"])

# Chat with image
result = client.chat_with_image(
    image_url="https://example.com/image.jpg",
    prompt="Describe this image"
)
```

### File Upload

```python
result = client.upload_file("video.mp4")
asset_id = result["data"]["asset_id"]
```

### YouTube Transcript

```python
result = client.youtube_transcript(
    video_url="https://www.youtube.com/watch?v=...",
    channel="channel_name"  # Required
)
# Returns: {"data": [{"start": "0.0", "dur": "5.0", "text": "..."}]}
```

### Embeddings

```python
# Text embeddings
result = client.text_embedding(
    texts=["text1", "text2"],
    model="gemini-embedding-001",
    dimensionality=512
)

# Video embeddings (requires uploaded video)
result = client.video_embedding(
    asset_id="re_123456789",
    model="multimodalembedding@001"
)

# Image embeddings
result = client.image_embedding(
    image_url="https://example.com/image.jpg"
)
# or from file
result = client.image_embedding(file_path="image.jpg")
```

## CLI Usage

```bash
# Text chat
python3 scripts/memories_client.py chat-text "Hello"

# Video chat
python3 scripts/memories_client.py chat --video "URL" --prompt "What's in this?"

# Image chat
python3 scripts/memories_client.py chat --image "URL" --prompt "Describe this"

# File upload
python3 scripts/memories_client.py upload /path/to/file.mp4

# YouTube transcript (channel required)
python3 scripts/memories_client.py youtube-transcript "URL" --channel "channel_name"

# Text embeddings
python3 scripts/memories_client.py embed-text "text1" "text2"

# Video embeddings
python3 scripts/memories_client.py embed-video "re_asset_id"

# Image embeddings
python3 scripts/memories_client.py embed-image --url "URL"
```

## API Format

### Chat Completion

```python
{
    "model": "qwen:qwen3-vl-plus",
    "messages": [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Your prompt"}  # String, NOT array!
    ]
}
```

### Text Embeddings

```python
{
    "input": ["text1", "text2"],
    "model": "gemini-embedding-001",
    "dimensionality": 512
}
```

### Video Embeddings

```python
{
    "asset_id": "re_xxx",
    "model": "multimodalembedding@001"
}
```
