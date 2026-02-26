#!/usr/bin/env python3
"""
Memories.ai Minimal Test Script

Tests the basic functionality of the memories.ai API.
WARNING: These tests use minimal tokens.
"""

import os
import sys
import requests
from pathlib import Path

# Configuration
API_KEY = os.environ.get("MEMORIES_AI_API_KEY", "")
BASE_URL = "https://mavi-backend.memories.ai/serve/api/v2"

def get_headers():
    return {"Authorization": API_KEY}


def test_upload_file():
    """Test 1: Upload a small text file"""
    print("\n=== Test 1: Upload File ===")
    try:
        url = f"{BASE_URL}/upload"
        files = {"file": ("test.txt", b"hello world", "text/plain")}
        resp = requests.post(url, headers=get_headers(), files=files)
        
        if resp.status_code == 200 and resp.json().get("success"):
            data = resp.json()["data"]
            asset_id = data.get("asset_id")
            print(f"✓ Upload successful! Asset ID: {asset_id}")
            return asset_id
        else:
            print(f"✗ Upload failed: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def test_list_videos():
    """Test 2: List uploaded videos"""
    print("\n=== Test 2: List Videos ===")
    try:
        # This endpoint may not be supported - just check
        url = f"{BASE_URL}/list-videos"
        resp = requests.get(url, headers=get_headers())
        print(f"Response: {resp.status_code} - {resp.text[:200]}")
        return resp.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_asset_info(asset_id):
    """Test 3: Get asset metadata"""
    print("\n=== Test 3: Get Asset Metadata ===")
    if not asset_id:
        print("⊘ Skipped (no asset_id)")
        return False
    
    try:
        url = f"{BASE_URL}/get-metadata"
        resp = requests.get(url, headers=get_headers(), params={"asset_id": asset_id})
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:300]}")
        return resp.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("Memories.ai API - Minimal Test Suite")
    print("=" * 50)
    
    if not API_KEY:
        print("ERROR: Set MEMORIES_AI_API_KEY environment variable")
        print("Usage: MEMORIES_AI_API_KEY=your_key python test_memories.py")
        sys.exit(1)
    
    print(f"API Key: {API_KEY[:20]}...")
    
    # Run tests
    results = {}
    
    # Test 1: Upload
    asset_id = test_upload_file()
    results["upload"] = asset_id is not None
    
    # Test 2: List (optional)
    results["list"] = test_list_videos()
    
    # Test 3: Get metadata
    results["metadata"] = test_asset_info(asset_id)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test}: {status}")
    
    all_passed = all(results.values())
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
