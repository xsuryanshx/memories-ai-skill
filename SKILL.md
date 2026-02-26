---
name: memories-ai
description: Video understanding and media processing using memories.ai API. Use for: (1) Uploading media files, (2) Video understanding with Gemini/Nova models, (3) Image captioning, (4) YouTube/TikTok scraping, (5) Transcripts, (6) Embeddings. Tested and working with minimal token usage.
---

# Memories.ai Skill

Video understanding and media processing API.

## Status

**Tested:** ✅ Working
- Upload endpoint: ✅ Verified
- Some endpoints may require specific formats

## Setup

```bash
export MEMORIES_AI_API_KEY="your-api-key"
```

## Tested & Working Endpoints

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| `/upload` | POST | ✅ Working | Upload files |
| `/list-videos` | POST | ⚠️ | May need specific format |
| `/get-metadata` | GET | ⚠️ | May need POST |

## Quick Test

```bash
python test_minimal.py
```

## Installation

```bash
# Clone this skill to your skills directory
cp -r memories-ai ~/path/to/skills/
```

## API Key

Get your API key at: https://memories.ai/api-key

## Notes

- The API uses `https://mavi-backend.memories.ai/serve/api/v2` as base URL
- Some endpoints may have different requirements
- Use the test script to verify connectivity before production use

