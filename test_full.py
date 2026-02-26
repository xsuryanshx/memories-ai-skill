#!/usr/bin/env python3
"""
Memories.ai Complete Test Suite

Tests key endpoints with MINIMAL token usage.
Each test is designed to use the least amount of tokens possible.
"""

import os
import sys
import requests
import json

# Configuration
API_KEY = os.environ.get("MEMORIES_AI_API_KEY", "")
BASE_URL = "https://mavi-backend.memories.ai/serve/api/v2"

def get_headers(content_type="application/json"):
    headers = {"Authorization": API_KEY}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


# ============================================================================
# TEST 1: Upload File (MOST RELIABLE)
# ============================================================================
def test_upload_file():
    """Test: Upload a small text file"""
    print("\n[TEST 1] Upload File")
    try:
        url = f"{BASE_URL}/upload"
        files = {"file": ("test.txt", b"hi", "text/plain")}
        resp = requests.post(url, headers=get_headers(None), files=files)
        
        result = resp.json()
        if result.get("success"):
            asset_id = result["data"]["asset_id"]
            print(f"  ✓ Uploaded: {asset_id}")
            return asset_id
        else:
            print(f"  ✗ Failed: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


# ============================================================================
# TEST 2: Upload Small Image
# ============================================================================
def test_upload_image():
    """Test: Upload a tiny image (1x1 pixel)"""
    print("\n[TEST 2] Upload Small Image")
    try:
        # Tiny 1x1 PNG (base64 encoded)
        tiny_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        
        url = f"{BASE_URL}/upload-image-from-file"
        files = {"file": ("tiny.png", tiny_png, "image/png")}
        resp = requests.post(url, headers=get_headers(None), files=files)
        
        result = resp.json()
        if result.get("success"):
            asset_id = result["data"]["asset_id"]
            print(f"  ✓ Image uploaded: {asset_id}")
            return asset_id
        else:
            print(f"  ✗ Response: {result.get('msg', result)}")
            return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


# ============================================================================
# TEST 3: Video Understanding (with text only - no video)
# ============================================================================
def test_chat_text_only():
    """Test: Chat completion with text only (minimal tokens)"""
    print("\n[TEST 3] Chat - Text Only")
    try:
        url = f"{BASE_URL}/vu/chat/completions"
        
        # Use minimal prompt
        data = {
            "model": "gemini:gemini-2.0-flash",
            "messages": [
                {"role": "user", "content": "Hi"}
            ],
            "max_tokens": 3  # Minimal!
        }
        
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("status") == "completed":
            content = result["choices"][0]["message"]["content"]
            print(f"  ✓ Response: {content[:50]}")
            return True
        elif result.get("error"):
            print(f"  ⚠ Error: {result['error'].get('message', 'unknown')[:100]}")
            return False
        else:
            print(f"  ⚠ Status: {result.get('status')}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================================
# TEST 4: Text Embeddings
# ============================================================================
def test_text_embedding():
    """Test: Generate text embedding (very minimal)"""
    print("\n[TEST 4] Text Embedding")
    try:
        url = f"{BASE_URL}/embeddings/text"
        
        data = {
            "text": "hi"  # Minimal!
        }
        
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            embedding = result["data"].get("embedding", [])
            print(f"  ✓ Got embedding, dimension: {len(embedding)}")
            return True
        else:
            print(f"  ✗ Response: {result.get('msg', result)[:100]}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================================
# TEST 5: Image Caption (using uploaded image)
# ============================================================================
def test_image_caption(asset_id):
    """Test: Caption an uploaded image"""
    print("\n[TEST 5] Image Caption")
    if not asset_id:
        print("  ⊘ Skipped (no asset)")
        return False
    
    try:
        url = f"{BASE_URL}/image/caption"
        
        data = {
            "asset_id": asset_id,
            "prompt": "Describe this image"
        }
        
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            caption = result["data"].get("caption", "")
            print(f"  ✓ Caption: {caption[:80]}")
            return True
        else:
            print(f"  ✗ Response: {result.get('msg', result)[:100]}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================================
# TEST 6: Delete Asset
# ============================================================================
def test_delete_asset(asset_id):
    """Test: Delete an asset"""
    print("\n[TEST 6] Delete Asset")
    if not asset_id:
        print("  ⊘ Skipped (no asset)")
        return False
    
    try:
        url = f"{BASE_URL}/delete"
        
        data = {"asset_id": asset_id}
        
        resp = requests.post(url, headers=get_headers(), json=data)
        result = resp.json()
        
        if result.get("success"):
            print(f"  ✓ Deleted: {asset_id}")
            return True
        else:
            print(f"  ✗ Response: {result.get('msg', result)[:100]}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================================
# TEST 7: Health Check
# ============================================================================
def test_health():
    """Test: Basic connectivity"""
    print("\n[TEST 7] Health Check")
    try:
        url = f"{BASE_URL}/health"
        resp = requests.get(url, timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.text[:100]}")
        return resp.status_code == 200
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("Memories.ai API - Complete Test Suite")
    print("=" * 60)
    
    if not API_KEY:
        print("\nERROR: Set MEMORIES_AI_API_KEY")
        print("Usage: MEMORIES_AI_API_KEY=your_key python test_full.py")
        sys.exit(1)
    
    print(f"\nAPI Key: {API_KEY[:15]}...")
    
    results = {}
    
    # Run tests in order
    results["health"] = test_health()
    results["upload_file"] = test_upload_file()
    results["upload_image"] = test_upload_image()
    results["chat_text"] = test_chat_text_only()
    results["text_embedding"] = test_text_embedding()
    
    # Use the text file asset for image caption test
    results["image_caption"] = test_image_caption(results.get("upload_file"))
    
    # Clean up
    results["delete"] = test_delete_asset(results.get("upload_file"))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for name, result in results.items():
        status = "✓ PASS" if result is True else ("✗ FAIL" if result is False else "⊘ SKIP")
        print(f"  {name}: {status}")
    
    print(f"\nPassed: {passed} | Failed: {failed} | Skipped: {skipped}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
