# Memories.ai Skill for OpenClaw

Video understanding and media processing using the memories.ai API.

## Features

- File upload
- Video understanding with Gemini/Nova models
- Image captioning
- YouTube/TikTok scraping
- Transcripts
- Embeddings
- And more...

## API Status

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/upload` | ✅ Working | File upload confirmed |
| Chat/Video Understanding | ⚠️ Issues | API backend errors |
| YouTube | ⚠️ Issues | Network errors |
| ILM (GPT) | ⚠️ Issues | Network errors |

**Note:** The API key authentication works. Some endpoints may require additional configuration or permissions.

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
# Run working tests
python test_working.py

# Run all tests
python test_full.py
```

## Usage

### Upload a File

```python
import requests

API_KEY = "your-key"
url = "https://mavi-backend.memories.ai/serve/api/v2/upload"
files = {"file": ("myfile.txt", b"content", "text/plain")}

response = requests.post(url, headers={"Authorization": API_KEY}, files=files)
print(response.json())
```

### Python Client

See `scripts/memories_client.py` for a full Python client.

## Files

- `SKILL.md` - Skill documentation
- `scripts/memories_client.py` - Python client
- `test_working.py` - Working test suite
- `test_full.py` - Full test suite
- `TEST_RESULTS.md` - Test results log

## Troubleshooting

If endpoints return errors:
1. Verify your API key is valid
2. Check network connectivity
3. Contact memories.ai support

## License

MIT

## Author

Built for OpenClaw by @xsuryanshx
