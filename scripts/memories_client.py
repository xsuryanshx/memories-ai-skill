#!/usr/bin/env python3
"""
Memories.ai Complete Python Client

Full video understanding, platform, and streaming API client.

Usage:
    python memories_client.py <command> [options]

Commands:
    chat            Chat with video/image
    caption-video   Generate video caption
    caption-image   Generate image caption
    upload          Upload file
    upload-url      Upload video from URL
    list-videos     List uploaded videos
    delete          Delete asset
    youtube-detail  Get YouTube video details
    youtube-transcript Get YouTube transcript
    youtube-comments Get YouTube comments
    search-memories Search memories
    search-video    Search private videos
    embed-video     Generate video embedding
    embed-image     Generate image embedding
    embed-text      Generate text embedding
    human-reid      Human re-identification
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Generator, List, Dict, Any


class MemoriesAIClient:
    """Complete client for memories.ai API."""
    
    BASE_URL = "https://mavi-backend.memories.ai/serve/api/v2"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MEMORIES_AI_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set MEMORIES_AI_API_KEY env var or pass --api-key")
        self.headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }
        self.headersMultipart = {
            "Authorization": f"{self.api_key}"
        }
    
    # ==================== UPLOAD ====================
    
    def upload_file(self, file_path: str) -> dict:
        """Upload a file to storage."""
        with open(file_path, 'rb') as f:
            resp = requests.post(
                f"{self.BASE_URL}/upload",
                headers=self.headersMultipart,
                files={"file": f}
            )
        resp.raise_for_status()
        return resp.json()
    
    def upload_video_from_url(self, video_url: str) -> dict:
        """Upload video from direct URL."""
        resp = requests.post(
            f"{self.BASE_URL}/upload-from-url",
            headers=self.headers,
            json={"video_url": video_url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def upload_image_from_file(self, file_path: str) -> dict:
        """Upload image from file."""
        with open(file_path, 'rb') as f:
            resp = requests.post(
                f"{self.BASE_URL}/upload-image-from-file",
                headers=self.headersMultipart,
                files={"file": f}
            )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== CHAT ====================
    
    def chat_completion(
        self,
        model: str,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False,
        **kwargs
    ) -> dict:
        """Generate chat completion with video/image input."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs
        }
        resp = requests.post(
            f"{self.BASE_URL}/vu/chat/completions",
            headers=self.headers,
            json=payload
        )
        resp.raise_for_status()
        return resp.json()
    
    def chat_with_video(
        self,
        video_url: str,
        prompt: str,
        model: str = "gemini:gemini-2.5-flash",
        **kwargs
    ) -> dict:
        """Chat with a video."""
        messages = [
            {"role": "system", "content": "You are a helpful video understanding assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "input_file", "file_uri": video_url, "mime_type": "video/mp4"}
            ]}
        ]
        return self.chat_completion(model, messages, **kwargs)
    
    def chat_with_image(
        self,
        image_url: str,
        prompt: str,
        model: str = "gemini:gemini-2.5-flash",
        **kwargs
    ) -> dict:
        """Chat with an image."""
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "input_file", "file_uri": image_url, "mime_type": "image/jpeg"}
            ]}
        ]
        return self.chat_completion(model, messages, **kwargs)
    
    def caption_video(self, video_url: str, prompt: str = "Describe this video") -> dict:
        """Generate caption for video."""
        return self.chat_with_video(video_url, prompt)
    
    def caption_image(self, image_url: str, prompt: str = "Describe this image") -> dict:
        """Generate caption for image."""
        return self.chat_with_image(image_url, prompt)
    
    # ==================== SEARCH ====================
    
    def search_memories(self, query: str, limit: int = 10) -> dict:
        """Semantic search across memories."""
        resp = requests.post(
            f"{self.BASE_URL}/search-memories",
            headers=self.headers,
            json={"query": query, "limit": limit}
        )
        resp.raise_for_status()
        return resp.json()
    
    def search_private_video(self, query: str) -> dict:
        """Search within private video library."""
        resp = requests.post(
            f"{self.BASE_URL}/search-private-video",
            headers=self.headers,
            json={"query": query}
        )
        resp.raise_for_status()
        return resp.json()
    
    def search_public_video(self, query: str) -> dict:
        """Search public videos."""
        resp = requests.post(
            f"{self.BASE_URL}/search-public-video",
            headers=self.headers,
            json={"query": query}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== TRANSCRIPTS ====================
    
    def get_video_transcription(self, video_id: str) -> dict:
        """Get transcription for a video."""
        resp = requests.get(
            f"{self.BASE_URL}/video-transcription",
            headers=self.headers,
            params={"video_number": video_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    def get_audio_transcription(self, video_id: str) -> dict:
        """Get audio transcription."""
        resp = requests.get(
            f"{self.BASE_URL}/audio-transcription",
            headers=self.headers,
            params={"video_number": video_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== YOUTUBE ====================
    
    def youtube_video_detail(self, url: str) -> dict:
        """Get YouTube video metadata."""
        resp = requests.post(
            f"{self.BASE_URL}/youtube/video-detail",
            headers=self.headers,
            json={"url": url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def youtube_transcript(self, url: str) -> dict:
        """Get YouTube video transcript."""
        resp = requests.post(
            f"{self.BASE_URL}/youtube/video-transcript",
            headers=self.headers,
            json={"url": url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def youtube_comments(self, url: str, limit: int = 20) -> dict:
        """Get YouTube video comments."""
        resp = requests.post(
            f"{self.BASE_URL}/youtube/video-comments",
            headers=self.headers,
            json={"url": url, "limit": limit}
        )
        resp.raise_for_status()
        return resp.json()
    
    def youtube_comment_replies(self, url: str, comment_id: str, limit: int = 20) -> dict:
        """Get YouTube comment replies."""
        resp = requests.post(
            f"{self.BASE_URL}/youtube/video-comment-reply",
            headers=self.headers,
            json={"url": url, "comment_id": comment_id, "limit": limit}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== TIKTOK ====================
    
    def tiktok_video_detail(self, url: str) -> dict:
        """Get TikTok video metadata."""
        resp = requests.post(
            f"{self.BASE_URL}/tiktok/video-detail",
            headers=self.headers,
            json={"url": url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def tiktok_transcript(self, url: str) -> dict:
        """Get TikTok video transcript."""
        resp = requests.post(
            f"{self.BASE_URL}/tiktok/video-transcript",
            headers=self.headers,
            json={"url": url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def tiktok_comments(self, url: str, limit: int = 20) -> dict:
        """Get TikTok video comments."""
        resp = requests.post(
            f"{self.BASE_URL}/tiktok/video-comments",
            headers=self.headers,
            json={"url": url, "limit": limit}
        )
        resp.raise_for_for_status()
        return resp.json()
    
    # ==================== STREAMING ====================
    
    def start_video_stream(self, video_url: str, prompt: str) -> dict:
        """Start real-time video stream understanding."""
        resp = requests.post(
            f"{self.BASE_URL}/stream/video/start",
            headers=self.headers,
            json={"video_url": video_url, "prompt": prompt}
        )
        resp.raise_for_status()
        return resp.json()
    
    def stop_video_stream(self, task_id: str) -> dict:
        """Stop video stream processing."""
        resp = requests.post(
            f"{self.BASE_URL}/stream/video/stop",
            headers=self.headers,
            json={"task_id": task_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    def start_audio_stream(self, audio_url: str, prompt: str) -> dict:
        """Start audio stream transcription."""
        resp = requests.post(
            f"{self.BASE_URL}/stream/audio/start",
            headers=self.headers,
            json={"audio_url": audio_url, "prompt": prompt}
        )
        resp.raise_for_status()
        return resp.json()
    
    def stop_audio_stream(self, task_id: str) -> dict:
        """Stop audio stream."""
        resp = requests.post(
            f"{self.BASE_URL}/stream/audio/stop",
            headers=self.headers,
            json={"task_id": task_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== EMBEDDINGS ====================
    
    def video_embedding(self, video_url: str) -> dict:
        """Generate video embedding."""
        resp = requests.post(
            f"{self.BASE_URL}/embeddings/video",
,
            json={"video_url": video_url}
        )
            headers=self.headers        resp.raise_for_status()
        return resp.json()
    
    def image_embedding(self, image_url: str) -> dict:
        """Generate image embedding."""
        resp = requests.post(
            f"{self.BASE_URL}/embeddings/image",
            headers=self.headers,
            json={"image_url": image_url}
        )
        resp.raise_for_status()
        return resp.json()
    
    def text_embedding(self, text: str) -> dict:
        """Generate text embedding."""
        resp = requests.post(
            f"{self.BASE_URL}/embeddings/text",
            headers=self.headers,
            json={"text": text}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== ASSET MANAGEMENT ====================
    
    def list_videos(self, limit: int = 20, offset: int = 0) -> dict:
        """List uploaded videos."""
        resp = requests.get(
            f"{self.BASE_URL}/list-videos",
            headers=self.headers,
            params={"limit": limit, "offset": offset}
        )
        resp.raise_for_status()
        return resp.json()
    
    def delete_asset(self, asset_id: str) -> dict:
        """Delete an asset."""
        resp = requests.post(
            f"{self.BASE_URL}/delete",
            headers=self.headers,
            json={"asset_id": asset_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    def get_asset_metadata(self, asset_id: str) -> dict:
        """Get asset metadata."""
        resp = requests.get(
            f"{self.BASE_URL}/get-metadata",
            headers=self.headers,
            params={"asset_id": asset_id}
        )
        resp.raise_for_status()
        return resp.json()
    
    def download_asset(self, asset_id: str, output_path: str) -> dict:
        """Download asset to file."""
        resp = requests.get(
            f"{self.BASE_URL}/download",
            headers=self.headers,
            params={"asset_id": asset_id}
        )
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return {"saved_to": output_path}
    
    # ==================== VIDEO PROCESSING ====================
    
    def clip_video(self, video_url: str, start: int, end: int) -> dict:
        """Create a clip from video."""
        resp = requests.post(
            f"{self.BASE_URL}/video/clip",
            headers=self.headers,
            json={"video_url": video_url, "start": start, "end": end}
        )
        resp.raise_for_status()
        return resp.json()
    
    def extract_frames(self, video_url: str, interval: int = 1) -> dict:
        """Extract frames from video."""
        resp = requests.post(
            f"{self.BASE_URL}/extract-frames",
            headers=self.headers,
            json={"video_url": video_url, "interval": interval}
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== HUMAN REID ====================
    
    def human_reid(self, reference_images: List[str], target_videos: List[str]) -> dict:
        """Identify/track people across videos."""
        resp = requests.post(
            f"{self.BASE_URL}/human-reid",
            headers=self.headers,
            json={
                "reference_images": reference_images,
                "target_videos": target_videos
            }
        )
        resp.raise_for_status()
        return resp.json()
    
    # ==================== MEMORY ====================
    
    def add_memory(self, content: str, tags: List[str] = None, **kwargs) -> dict:
        """Add a memory."""
        data = {"content": content}
        if tags:
            data["tags"] = tags
        data.update(kwargs)
        resp = requests.post(
            f"{self.BASE_URL}/add-memory",
            headers=self.headers,
            json=data
        )
        resp.raise_for_status()
        return resp.json()
    
    def list_memories(self, query: str = None, tags: List[str] = None, limit: int = 10) -> dict:
        """List memories."""
        data = {"limit": limit}
        if query:
            data["query"] = query
        if tags:
            data["tags"] = tags
        resp = requests.get(
            f"{self.BASE_URL}/list-memories",
            headers=self.headers,
            params=data
        )
        resp.raise_for_status()
        return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="Memories.ai Complete Python Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--api-key", help="API key (or set MEMORIES_AI_API_KEY)")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Chat
    chat_parser = subparsers.add_parser("chat", help="Chat with video/image")
    chat_parser.add_argument("--video", help="Video URL")
    chat_parser.add_argument("--image", help="Image URL")
    chat_parser.add_argument("--prompt", required=True, help="Prompt")
    chat_parser.add_argument("--model", default="gemini:gemini-2.5-flash", help="Model")
    chat_parser.add_argument("--temp", type=float, default=0.7, help="Temperature")
    chat_parser.add_argument("--max-tokens", type=int, default=1000, help="Max tokens")
    
    # Caption
    cap_v_parser = subparsers.add_parser("caption-video", help="Caption video")
    cap_v_parser.add_argument("--url", required=True, help="Video URL")
    cap_v_parser.add_argument("--prompt", default="Describe this video", help="Prompt")
    
    cap_i_parser = subparsers.add_parser("caption-image", help="Caption image")
    cap_i_parser.add_argument("--url", required=True, help="Image URL")
    cap_i_parser.add_argument("--prompt", default="Describe this image", help="Prompt")
    
    # Upload
    up_parser = subparsers.add_parser("upload", help="Upload file")
    up_parser.add_argument("file", help="File path")
    
    up_url_parser = subparsers.add_parser("upload-url", help="Upload from URL")
    up_url_parser.add_argument("url", help="Video URL")
    
    # List/Delete
    list_parser = subparsers.add_parser("list-videos", help="List videos")
    list_parser.add_argument("--limit", type=int, default=20, help="Limit")
    list_parser.add_argument("--offset", type=int, default=0, help="Offset")
    
    del_parser = subparsers.add_parser("delete", help="Delete asset")
    del_parser.add_argument("asset_id", help="Asset ID")
    
    # YouTube
    yt_detail = subparsers.add_parser("youtube-detail", help="YouTube video details")
    yt_detail.add_argument("url", help="YouTube URL")
    
    yt_trans = subparsers.add_parser("youtube-transcript", help="YouTube transcript")
    yt_trans.add_argument("url", help="YouTube URL")
    
    yt_comm = subparsers.add_parser("youtube-comments", help="YouTube comments")
    yt_comm.add_argument("url", help="YouTube URL")
    yt_comm.add_argument("--limit", type=int, default=20, help="Limit")
    
    # Search
    search_mem = subparsers.add_parser("search-memories", help="Search memories")
    search_mem.add_argument("query", help="Search query")
    search_mem.add_argument("--limit", type=int, default=10, help="Limit")
    
    search_vid = subparsers.add_parser("search-video", help="Search private videos")
    search_vid.add_argument("query", help="Search query")
    
    # Embeddings
    emb_vid = subparsers.add_parser("embed-video", help="Video embedding")
    emb_vid.add_argument("url", help="Video URL")
    
    emb_img = subparsers.add_parser("embed-image", help="Image embedding")
    emb_img.add_argument("url", help="Image URL")
    
    emb_txt = subparsers.add_parser("embed-text", help="Text embedding")
    emb_txt.add_argument("text", help="Text")
    
    # Human ReID
    reid = subparsers.add_parser("human-reid", help="Human re-identification")
    reid.add_argument("--ref", nargs="+", required=True, help="Reference images")
    reid.add_argument("--target", nargs="+", required=True, help="Target videos")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        client = MemoriesAIClient(api_key=args.api_key)
        
        if args.command == "chat":
            if args.video:
                result = client.chat_with_video(args.video, args.prompt, args.model, temperature=args.temp, max_tokens=args.max_tokens)
            elif args.image:
                result = client.chat_with_image(args.image, args.prompt, args.model, temperature=args.temp, max_tokens=args.max_tokens)
            else:
                print("Error: --video or --image required")
                return
            print(json.dumps(result, indent=2))
            
        elif args.command == "caption-video":
            result = client.caption_video(args.url, args.prompt)
            print(json.dumps(result, indent=2))
            
        elif args.command == "caption-image":
            result = client.caption_image(args.url, args.prompt)
            print(json.dumps(result, indent=2))
            
        elif args.command == "upload":
            result = client.upload_file(args.file)
            print(json.dumps(result, indent=2))
            
        elif args.command == "upload-url":
            result = client.upload_video_from_url(args.url)
            print(json.dumps(result, indent=2))
            
        elif args.command == "list-videos":
            result = client.list_videos(args.limit, args.offset)
            print(json.dumps(result, indent=2))
            
        elif args.command == "delete":
            result = client.delete_asset(args.asset_id)
            print(json.dumps(result, indent=2))
            
        elif args.command == "youtube-detail":
            result = client.youtube_video_detail(args.url)
            print(json.dumps(result, indent=2))
            
        elif args.command == "youtube-transcript":
            result = client.youtube_transcript(args.url)
            print(json.dumps(result, indent=2))
            
        elif args.command == "youtube-comments":
            result = client.youtube_comments(args.url, args.limit)
            print(json.dumps(result, indent=2))
            
        elif args.command == "search-memories":
            result = client.search_memories(args.query, args.limit)
            print(json.dumps(result, indent=2))
            
        elif args.command == "search-video":
            result = client.search_private_video(args.query)
            print(json.dumps(result, indent=2))
            
        elif args.command == "embed-video":
            result = client.video_embedding(args.url)
            print(json.dumps(result, indent=2))
            
        elif args.command == "embed-image":
            result = client.image_embedding(args.url)
            print(json.dumps(result, indent=2))
            
        elif args.command == "embed-text":
            result = client.text_embedding(args.text)
            print(json.dumps(result, indent=2))
            
        elif args.command == "human-reid":
            result = client.human_reid(args.ref, args.target)
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
