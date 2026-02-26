# Memories.ai Skill for Claude Code

Video understanding and media processing using the memories.ai API.

## Features

- File upload
- Video understanding with Qwen VL models
- Image captioning
- YouTube transcript extraction
- Text/image/video embeddings

## API Status

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/upload` | ✅ Working | Multipart file upload |
| `/vu/chat/completions` | ✅ Working | Use `qwen:qwen3-vl-plus` model |
| `/youtube/video/transcript` | ✅ Working | Requires channel parameter |
| `/embeddings/text` | ✅ Working | Use `input` array |
| `/embeddings/video` | ✅ Working | Requires video asset_id |
| `/embeddings/image` | ✅ Working | File or URL |

## Installation

```bash
# Clone to your skills directory
git clone https://github.com/xsuryanshx/memories-ai-skill.git
```

## Configuration

Set your API key:

```bash
export MEMORIES_AI_API_KEY="your-api-key"
```

Get your API key at: https://memories.ai/api-key

## Quick Test

```bash
# Text chat
python3 scripts/memories_client.py chat-text "Hello"

# Video chat
python3 scripts/memories_client.py chat --video "URL" --prompt "What's in this?"

# YouTube transcript
python3 scripts/memories_client.py youtube-transcript "URL" --channel "channel_name"
```

## Usage

### Python Client

```python
from scripts.memories_client import MemoriesAIClient

client = MemoriesAIClient(api_key="your-key")

# Text chat
result = client.chat_text("Hello!")
print(result["choices"][0]["text"])

# Video chat
result = client.chat_with_video(
    video_url="https://example.com/video.mp4",
    prompt="What's in this?"
)

# Image chat
result = client.chat_with_image(
    image_url="https://example.com/image.jpg",
    prompt="Describe this"
)

# File upload
result = client.upload_file("video.mp4")
asset_id = result["data"]["asset_id"]

# YouTube transcript
result = client.youtube_transcript(
    video_url="https://www.youtube.com/watch?v=...",
    channel="channel_name"
)

# Text embeddings
result = client.text_embedding(texts=["text1", "text2"])

# Video embeddings
result = client.video_embedding(asset_id="re_xxx")

# Image embeddings
result = client.image_embedding(image_url="https://...")
```

### CLI Commands

```bash
# Text chat
python3 scripts/memories_client.py chat-text "Hello"

# Video chat
python3 scripts/memories_client.py chat --video "URL" --prompt "What's in this?"

# Image chat
python3 scripts/memories_client.py chat --image "URL" --prompt "Describe this"

# File upload
python3 scripts/memories_client.py upload /path/to/file.mp4

# YouTube transcript
python3 scripts/memories_client.py youtube-transcript "URL" --channel "channel_name"

# Text embeddings
python3 scripts/memories_client.py embed-text "text1" "text2"

# Video embeddings
python3 scripts/memories_client.py embed-video "re_asset_id"

# Image embeddings
python3 scripts/memories_client.py embed-image --url "URL"
```

## Files

- `SKILL.md` - Skill documentation
- `scripts/memories_client.py` - Python client
- `TEST_RESULTS.md` - Test results log

## License

MIT

## Author

Built for Claude Code by @xsuryanshx
