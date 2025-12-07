#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse

# Default save location
OUTPUT_DIR = "/Users/mokrzesik/Desktop/Michael/Music/Youtube/Videos/Marching Illini"

def prompt_rename(original_title: str) -> str:
    print(f'\n🎬 Current video title: "{original_title}"')
    new_name = input("Enter new name (or leave blank to keep original): ").strip()
    return new_name if new_name else original_title

def get_video_title(url: str) -> str:
    """Fetch the video title using yt-dlp (without downloading)."""
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def build_format_string(fmt: str, max_height: int | None):
    """
    Build yt-dlp format selector and merge options for the chosen container.
    - mp4  → bestvideo[ext=mp4]+bestaudio[ext=m4a]
    - webm → bestvideo[ext=webm]+bestaudio[ext=webm]
    - mkv  → bestvideo+bestaudio (any codecs), merge into mkv
    """
    height_filter = f"[height<=?{max_height}]" if max_height else ""
    if fmt == "mp4":
        format_str = f"bestvideo{height_filter}[ext=mp4]+bestaudio[ext=m4a]/best{height_filter}[ext=mp4]"
        merge_ext = "mp4"
        out_ext = "mp4"
    elif fmt == "webm":
        format_str = f"bestvideo{height_filter}[ext=webm]+bestaudio[ext=webm]/best{height_filter}[ext=webm]"
        merge_ext = "webm"
        out_ext = "webm"
    elif fmt == "mkv":
        format_str = f"bestvideo{height_filter}+bestaudio/best{height_filter}"
        merge_ext = "mkv"
        out_ext = "mkv"
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    return format_str, merge_ext, out_ext

def download_video(url: str, final_filename: str, fmt: str, max_height: int | None, output_dir: str):
    """Perform the actual download and merging process."""
    fmt_str, merge_ext, out_ext = build_format_string(fmt, max_height)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{final_filename}.{out_ext}")

    print(f"⬇️ Downloading as {fmt.upper()}"
          f"{f' (≤{max_height}p)' if max_height else ''} → {output_path}")
    subprocess.run([
        "yt-dlp",
        "-f", fmt_str,
        "--merge-output-format", merge_ext,
        "-o", output_path,
        url
    ], check=True)

    print(f"✅ Done! Video saved to: {output_path}")

def update_yt_dlp():
    """Ensure yt-dlp is current."""
    print("🔄 Updating yt-dlp to the latest version...")
    subprocess.run(["brew", "upgrade", "yt-dlp"], check=True)
    print("✅ yt-dlp updated.")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos as MP4, WEBM, or MKV."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-mp4", "--mp4", dest="fmt", action="store_const", const="mp4",
                       help="Download and merge into MP4 (H.264 + AAC/M4A)")
    group.add_argument("-webm", "--webm", dest="fmt", action="store_const", const="webm",
                       help="Download and merge into WEBM (VP9 + Opus)")
    group.add_argument("-mkv", "--mkv", dest="fmt", action="store_const", const="mkv",
                       help="Download and merge into MKV (any codecs)")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--max-height", type=int, default=None,
                        help="Prefer streams with height ≤ this value (e.g., 1080, 720)")
    parser.add_argument("--output-dir", default=OUTPUT_DIR,
                        help=f"Custom output directory (default: {OUTPUT_DIR})")
    return parser.parse_args()

def main():
    if len(sys.argv) == 1:
        print("Usage: uv run download_youtube_video.py -mp4|--webm|--mkv <YouTube_URL> [--max-height 1080] [--output-dir PATH]")
        sys.exit(1)

    args = parse_args()
    update_yt_dlp()

    try:
        title = get_video_title(args.url)
        final_name = prompt_rename(title)
        download_video(args.url, final_name, args.fmt, args.max_height, args.output_dir)
    except subprocess.CalledProcessError as e:
        print("❌ Error during download or merge:")
        print(e)

if __name__ == "__main__":
    main()
