#!/usr/bin/env python3
"""
Memories.ai Working Test Suite

Tests only the endpoints that are confirmed to work.
"""

import os
import sys
import requests

API_KEY = os.environ.get("MEMORIES_AI_API_KEY", "")
BASE_URL = "https://mavi-backend.memories.ai/serve/api/v2"

def get_headers():
    return {"Authorization": API_KEY}


def test_upload():
    """Test file upload - MOST RELIABLE"""
    print("\n[1] File Upload")
    try:
        url = f"{BASE_URL}/upload"
        files = {"file": ("test.txt", b"test content", "text/plain")}
        resp = requests.post(url, headers=get_headers(), files=files)
        result = resp.json()
        
        if result.get("success"):
            asset_id = result["data"]["asset_id"]
            print(f"    ✓ Uploaded: {asset_id}")
            return asset_id
        print(f"    ✗ {result.get('msg')}")
        return None
    except Exception as e:
        print(f"    ✗ {e}")
        return None


def test_upload_image():
    """Test image upload"""
    print("\n[2] Image Upload")
    try:
        # Tiny valid PNG (1x1 red pixel)
        import base64
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        )
        
        url = f"{BASE_URL}/upload-image-from-file"
        files = {"file": ("test.png", png_data, "image/png")}
        resp = requests.post(url, headers=get_headers(), files=files)
        result = resp.json()
        
        if result.get("success"):
            asset_id = result["data"]["asset_id"]
            print(f"    ✓ Uploaded image: {asset_id}")
            return asset_id
        print(f"    ⚠ {result.get('msg')}")
        return None
    except Exception as e:
        print(f"    ✗ {e}")
        return None


def test_video_upload_url():
    """Test video upload from URL"""
    print("\n[3] Video Upload from URL")
    try:
        # Try with a small public video URL
        url = f"{BASE_URL}/upload-video-from-url"
        
        # Use a small test video
        data = {"video_url": "https://www.w3schools.com/html/mov_bbb.mp4"}
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            asset_id = result["data"]["asset_id"]
            print(f"    ✓ Uploaded video: {asset_id}")
            return asset_id
        print(f"    ⚠ {result.get('msg')[:80]}")
        return None
    except Exception as e:
        print(f"    ✗ {e}")
        return None


def test_youtube_transcript():
    """Test YouTube transcript"""
    print("\n[4] YouTube Transcript")
    try:
        url = f"{BASE_URL}/youtube/video-transcript"
        data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            transcript = result["data"].get("transcript", "")[:100]
            print(f"    ✓ Got transcript: {transcript}...")
            return True
        print(f"    ⚠ {result.get('msg', 'failed')[:80]}")
        return False
    except Exception as e:
        print(f"    ✗ {e}")
        return False


def test_youtube_detail():
    """Test YouTube video detail"""
    print("\n[5] YouTube Video Detail")
    try:
        url = f"{BASE_URL}/youtube/video-detail"
        data = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            title = result["data"].get("title", "unknown")
            print(f"    ✓ Video: {title[:50]}")
            return True
        print(f"    ⚠ {result.get('msg', 'failed')[:80]}")
        return False
    except Exception as e:
        print(f"    ✗ {e}")
        return False


def test_ilm_chat():
    """Test ILM (Image Language Model) chat"""
    print("\n[6] ILM Chat (GPT)")
    try:
        url = f"{BASE_URL}/ilm/chat/completions"
        data = {
            "model": "gpt:gpt-4o-mini",
            "messages": [{"role": "user", "content": "Say hi in 3 words"}],
            "max_tokens": 10
        }
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("status") == "completed":
            content = result["choices"][0]["message"]["content"]
            print(f"    ✓ Response: {content[:50]}")
            return True
        print(f"    ⚠ {result.get('error', {}).get('message', 'failed')[:80]}")
        return False
    except Exception as e:
        print(f"    ✗ {e}")
        return False


def test_delete(asset_id):
    """Test delete"""
    if not asset_id:
        return False
    print("\n[7] Delete Asset")
    try:
        url = f"{BASE_URL}/delete"
        data = {"asset_id": asset_id}
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            print(f"    ✓ Deleted")
            return True
        print(f"    ⚠ {result.get('msg', 'failed')}")
        return False
    except Exception as e:
        print(f"    ✗ {e}")
        return False


def main():
    print("=" * 50)
    print("Memories.ai - Working Tests")
    print("=" * 50)
    
    if not API_KEY:
        print("\nERROR: Set MEMORIES_AI_API_KEY")
        sys.exit(1)
    
    print(f"\nKey: {API_KEY[:15]}...")
    
    results = {}
    
    # Run tests
    results["upload"] = test_upload()
    results["image"] = test_upload_image()
    results["video"] = test_video_upload_url()
    results["youtube_transcript"] = test_youtube_transcript()
    results["youtube_detail"] = test_youtube_detail()
    results["ilm_chat"] = test_ilm_chat()
    results["delete"] = test_delete(results.get("upload"))
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v is True)
    assets = sum(1 for v in results.values() if isinstance(v, str) and v.startswith("re_"))
    failed = len(results) - passed - assets
    
    print(f"  Upload/Assets: {assets}")
    print(f"  Passed: {passed}")
    print(f"  Failed/Skipped: {failed}")
    
    if assets > 0:
        print(f"\n  ✓ Got {assets} asset ID(s) for further use!")


if __name__ == "__main__":
    main()
