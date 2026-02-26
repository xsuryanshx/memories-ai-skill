#!/usr/bin/env python3
"""
Memories.ai Python Client

A Python client for the memories.ai video understanding API.

Usage:
    python memories_client.py <command> [options]

Commands:
    chat            Chat with video/image
    chat-text       Text-only chat
    caption-video   Generate video caption
    caption-image   Generate image caption
    upload          Upload file
    youtube-transcript Get YouTube transcript
    embed-video     Generate video embedding
    embed-image     Generate image embedding
    embed-text      Generate text embedding
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, List, Dict


class MemoriesAIClient:
    """Client for memories.ai API."""

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
        model: str = "qwen:qwen3-vl-plus",
        **kwargs
    ) -> dict:
        """Chat with a video."""
        messages = [
            {"role": "system", "content": "You are a helpful video understanding assistant."},
            {"role": "user", "content": f"{prompt}\n\n[Video: {video_url}]"}
        ]
        return self.chat_completion(model, messages, **kwargs)

    def chat_with_image(
        self,
        image_url: str,
        prompt: str,
        model: str = "qwen:qwen3-vl-plus",
        **kwargs
    ) -> dict:
        """Chat with an image."""
        messages = [
            {"role": "user", "content": f"{prompt}\n\n[Image: {image_url}]"}
        ]
        return self.chat_completion(model, messages, **kwargs)

    def chat_text(
        self,
        prompt: str,
        model: str = "qwen:qwen3-vl-plus",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ) -> dict:
        """Text-only chat (no video/image)."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        return self.chat_completion(model, messages, **kwargs)

    def caption_video(self, video_url: str, prompt: str = "Describe this video") -> dict:
        """Generate caption for video."""
        return self.chat_with_video(video_url, prompt)

    def caption_image(self, image_url: str, prompt: str = "Describe this image") -> dict:
        """Generate caption for image."""
        return self.chat_with_image(image_url, prompt)

    # ==================== YOUTUBE ====================

    def youtube_transcript(self, video_url: str, channel: str = None) -> dict:
        """Get YouTube video transcript."""
        payload = {"video_url": video_url}
        if channel:
            payload["channel"] = channel
        resp = requests.post(
            f"{self.BASE_URL}/youtube/video/transcript",
            headers=self.headers,
            json=payload
        )
        resp.raise_for_status()
        return resp.json()

    # ==================== EMBEDDINGS ====================

    def video_embedding(self, asset_id: str, model: str = "multimodalembedding@001") -> dict:
        """Generate video embedding."""
        resp = requests.post(
            f"{self.BASE_URL}/embeddings/video",
            headers=self.headers,
            json={"asset_id": asset_id, "model": model}
        )
        resp.raise_for_status()
        return resp.json()

    def image_embedding(self, file_path: str = None, image_url: str = None, model: str = "multimodalembedding@001") -> dict:
        """Generate image embedding from file or URL."""
        if file_path:
            with open(file_path, 'rb') as f:
                resp = requests.post(
                    f"{self.BASE_URL}/embeddings/image",
                    headers=self.headersMultipart,
                    files={"file": f},
                    data={"model": model}
                )
        elif image_url:
            resp = requests.post(
                f"{self.BASE_URL}/embeddings/image",
                headers=self.headers,
                json={"image_url": image_url, "model": model}
            )
        else:
            raise ValueError("Either file_path or image_url required")
        resp.raise_for_status()
        return resp.json()

    def text_embedding(self, texts: List[str], model: str = "gemini-embedding-001", dimensionality: int = 512) -> dict:
        """Generate text embedding."""
        resp = requests.post(
            f"{self.BASE_URL}/embeddings/text",
            headers=self.headers,
            json={"input": texts, "model": model, "dimensionality": dimensionality}
        )
        resp.raise_for_status()
        return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="Memories.ai Python Client",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--api-key", help="API key (or set MEMORIES_AI_API_KEY)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Chat
    chat_parser = subparsers.add_parser("chat", help="Chat with video/image")
    chat_parser.add_argument("--video", help="Video URL")
    chat_parser.add_argument("--image", help="Image URL")
    chat_parser.add_argument("--prompt", required=True, help="Prompt")
    chat_parser.add_argument("--model", default="qwen:qwen3-vl-plus", help="Model")
    chat_parser.add_argument("--temp", type=float, default=0.7, help="Temperature")
    chat_parser.add_argument("--max-tokens", type=int, default=1000, help="Max tokens")

    # Text Chat
    text_chat_parser = subparsers.add_parser("chat-text", help="Text-only chat")
    text_chat_parser.add_argument("prompt", help="Prompt")
    text_chat_parser.add_argument("--model", default="qwen:qwen3-vl-plus", help="Model")
    text_chat_parser.add_argument("--system", default="You are a helpful assistant.", help="System prompt")
    text_chat_parser.add_argument("--temp", type=float, default=0.7, help="Temperature")
    text_chat_parser.add_argument("--max-tokens", type=int, default=1000, help="Max tokens")

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

    # YouTube
    yt_trans = subparsers.add_parser("youtube-transcript", help="YouTube transcript")
    yt_trans.add_argument("url", help="YouTube URL")
    yt_trans.add_argument("--channel", help="YouTube channel (required)")

    # Embeddings
    emb_vid = subparsers.add_parser("embed-video", help="Video embedding")
    emb_vid.add_argument("asset_id", help="Video asset_id (e.g., re_657745568997527552)")
    emb_vid.add_argument("--model", default="multimodalembedding@001", help="Model")

    emb_img = subparsers.add_parser("embed-image", help="Image embedding")
    emb_img.add_argument("--file", help="Image file path")
    emb_img.add_argument("--url", help="Image URL")
    emb_img.add_argument("--model", default="multimodalembedding@001", help="Model")

    emb_txt = subparsers.add_parser("embed-text", help="Text embedding")
    emb_txt.add_argument("texts", nargs="+", help="Text strings to embed")
    emb_txt.add_argument("--model", default="gemini-embedding-001", help="Model")
    emb_txt.add_argument("--dim", type=int, default=512, help="Dimensionality")

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

        elif args.command == "chat-text":
            result = client.chat_text(args.prompt, args.model, args.system, temperature=args.temp, max_tokens=args.max_tokens)
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

        elif args.command == "youtube-transcript":
            result = client.youtube_transcript(args.url, args.channel)
            print(json.dumps(result, indent=2))

        elif args.command == "embed-video":
            result = client.video_embedding(args.asset_id, args.model)
            print(json.dumps(result, indent=2))

        elif args.command == "embed-image":
            result = client.image_embedding(file_path=args.file, image_url=args.url, model=args.model)
            print(json.dumps(result, indent=2))

        elif args.command == "embed-text":
            result = client.text_embedding(args.texts, args.model, args.dim)
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
