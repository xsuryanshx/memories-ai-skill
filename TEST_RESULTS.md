# Memories.ai Skill - Test Results

## Test Summary (Feb 2026)

### Working Endpoints ✅

| Endpoint | Status | Notes |
|----------|--------|-------|
| File Upload (`POST /upload`) | ✅ Working | Multipart file upload |
| Text Chat (`POST /vu/chat/completions`) | ✅ Working | Use `qwen:qwen3-vl-plus` model |
| Video Chat (`POST /vu/chat/completions`) | ✅ Working | Use video URL directly |
| Image Chat (`POST /vu/chat/completions`) | ✅ Working | Use image URL directly |
| YouTube Transcript (`POST /youtube/video/transcript`) | ✅ Working | Requires channel parameter |
| Text Embeddings (`POST /embeddings/text`) | ✅ Working | Use `input` array, `gemini-embedding-001` model |
| Video Embeddings (`POST /embeddings/video`) | ✅ Working | Requires valid video asset_id |
| Image Embeddings (`POST /embeddings/image`) | ✅ Working | File or URL |

### Not Working Endpoints ❌ (Removed from client)

| Endpoint | Status | Notes |
|----------|--------|-------|
| List Videos | ❌ | POST/GET not supported |
| Search Memories | ❌ | POST/GET not supported |
| Delete Asset | ❌ | POST not supported |
| YouTube Video Detail | ❌ | Network abnormal |
| YouTube Comments | ❌ | Not tested |

## Working API Formats

### Chat Completion (Text/Video/Image)
```python
# Text chat
{
    "model": "qwen:qwen3-vl-plus",
    "messages": [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "What is in this video?"}
    ]
}

# Video/Image chat - include URL in message content
{
    "model": "qwen:qwen3-vl-plus",
    "messages": [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "What is this?\n\n[Video: https://example.com/video.mp4]"}
    ]
}
# Returns: {"status": "completed", "choices": [{"text": "Description..."}]}
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
    "asset_id": "re_xxx",  # Must be a video asset
    "model": "multimodalembedding@001"
}
```

### Image Embeddings
```python
# Option 1: File upload
files = {'file': open('image.jpg', 'rb')}
data = {'model': 'multimodalembedding@001'}

# Option 2: URL
{
    "image_url": "https://...",
    "model": "multimodalembedding@001"
}
```

### File Upload
```python
files = {'file': ('filename', open('file', 'rb'))}
# POST /upload - multipart/form-data
# Returns: {"success": true, "data": {"asset_id": "re_xxx"}}
```

## Issues Encountered

1. **POST not supported**: Many endpoints (search-memories, list-videos, etc.) return "POST not supported"
2. **Network errors**: YouTube endpoints return "Network abnormal"
3. **Model requirements**: Chat requires `qwen:qwen3-vl-plus` model (not gemini)
4. **Content format**: Message content must be a string, not an array

## Client Usage

```bash
# Text chat
python3 scripts/memories_client.py chat-text "Hello"

# Video chat
python3 scripts/memories_client.py chat --video "URL" --prompt "What's in this?"

# Image chat
python3 scripts/memories_client.py chat --image "URL" --prompt "Describe this"

# Text embeddings
python3 scripts/memories_client.py embed-text "text1" "text2"

# Video embeddings (requires uploaded video asset)
python3 scripts/memories_client.py embed-video "re_xxx"

# File upload
python3 scripts/memories_client.py upload /path/to/file
```

## Recommendations

1. Use upload + chat (qwen) + embeddings as primary working endpoints
2. Contact memories.ai for updated API documentation on other endpoints
3. Some endpoints may require different API key tiers/permissions
