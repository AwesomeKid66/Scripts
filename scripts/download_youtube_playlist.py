#!/usr/bin/env python3
import subprocess
import sys
import os
import glob
import shutil
import json
import argparse

OUTPUT_DIR = "/Users/mokrzesik/Desktop/Michael/Music/Youtube"
TEMP_DIR = os.path.join(os.getcwd(), "yt_temp")

def prompt_rename(original_title: str) -> str:
    print(f'\n📝 Current filename: "{original_title}"')
    new_name = input("Enter new name (or leave blank to keep original): ").strip()
    return new_name if new_name else original_title

def get_title(url: str) -> str:
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def get_playlist_entries(url: str):
    print("📋 Fetching playlist entries...")
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "-J", url],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout)
    entries = data.get("entries", [])
    return [f"https://www.youtube.com/watch?v={entry['id']}" for entry in entries]

def try_direct_download(url: str, audio_format: str, output_dir: str) -> bool:
    """
    Direct path using yt-dlp:
      - mp3: extract & convert via ffmpeg (yt-dlp postprocess)
      - m4a: try native m4a stream to avoid re-encode
    """
    title = get_title(url)
    final_name = prompt_rename(title)
    os.makedirs(output_dir, exist_ok=True)

    if audio_format == "mp3":
        print("🎯 Attempting direct download & conversion to .mp3...")
        output_path = os.path.join(output_dir, f"{final_name}.mp3")
        result = subprocess.run([
            "yt-dlp",
            "-x", "--audio-format", "mp3", "--audio-quality", "192K",
            "-o", output_path,
            url
        ])
        return result.returncode == 0

    elif audio_format == "m4a":
        print("🎯 Attempting direct download as .m4a...")
        output_path = os.path.join(output_dir, f"{final_name}.m4a")
        result = subprocess.run([
            "yt-dlp",
            "-f", "bestaudio[ext=m4a]",
            "-o", output_path,
            url
        ])
        return result.returncode == 0

    else:
        print(f"❌ Unsupported format: {audio_format}")
        return False

def fallback_download_and_convert(url: str, audio_format: str, output_dir: str):
    print("⬇️ Direct approach failed, using fallback with manual conversion...")
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 1) Download best available audio to temp
    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-o", os.path.join(TEMP_DIR, "%(title)s.%(ext)s"),
        url
    ], check=True)

    # 2) Find newest fetched file
    audio_files = glob.glob(os.path.join(TEMP_DIR, "*.*"))
    if not audio_files:
        print("❌ No audio file found for conversion.")
        return

    input_file = max(audio_files, key=os.path.getctime)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    final_name = prompt_rename(base_name)

    if audio_format == "m4a":
        output_file = os.path.join(output_dir, final_name + ".m4a")
        print(f"🔁 Converting {input_file} → {output_file} (AAC 192k)...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_file,
            "-c:a", "aac", "-b:a", "192k",
            output_file
        ], check=True)
    elif audio_format == "mp3":
        output_file = os.path.join(output_dir, final_name + ".mp3")
        print(f"🔁 Converting {input_file} → {output_file} (MP3 192k)...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_file,
            "-codec:a", "libmp3lame", "-b:a", "192k",
            output_file
        ], check=True)
    else:
        print(f"❌ Unsupported format in fallback: {audio_format}")
        return

    # 3) Cleanup
    try:
        os.remove(input_file)
    except OSError:
        pass
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print(f"✅ Done! Saved to: {output_file}")

def process_video(url: str, audio_format: str, output_dir: str):
    if not try_direct_download(url, audio_format, output_dir):
        fallback_download_and_convert(url, audio_format, output_dir)

def update_yt_dlp():
    print("🔄 Updating yt-dlp to the latest version...")
    subprocess.run(["brew", "upgrade", "yt-dlp"], check=True)
    print("✅ yt-dlp updated.")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download audio from a single YouTube video or an entire playlist as MP3 or M4A."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-mp3", "--mp3", dest="format", action="store_const", const="mp3",
                       help="Download/convert to MP3")
    group.add_argument("-m4a", "--m4a", dest="format", action="store_const", const="m4a",
                       help="Download/convert to M4A")
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument("--output-dir", default=OUTPUT_DIR,
                        help=f"Directory to save files (default: {OUTPUT_DIR})")
    return parser.parse_args()

def main():
    if len(sys.argv) == 1:
        print("Usage: uv run download_playlist_audio.py -mp3|--m4a <YouTube_URL> [--output-dir PATH]")
        sys.exit(1)

    args = parse_args()
    url = args.url
    audio_format = args.format
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)
    update_yt_dlp()

    if "playlist?" in url or "list=" in url:
        print("🎧 Playlist detected. Processing all videos...")
        entries = get_playlist_entries(url)
        for idx, video_url in enumerate(entries, 1):
            print(f"\n🔹 [{idx}/{len(entries)}] {video_url}")
            try:
                process_video(video_url, audio_format, output_dir)
            except subprocess.CalledProcessError as e:
                print("❌ Error on this item; continuing to next.")
                print(e)
    else:
        print("🎵 Single video detected.")
        try:
            process_video(url, audio_format, output_dir)
        except subprocess.CalledProcessError as e:
            print("❌ An error occurred during download or conversion.")
            print(e)

if __name__ == "__main__":
    import argparse  # ensure argparse is available when run directly
    main()