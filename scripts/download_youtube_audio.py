#!/usr/bin/env python3
import subprocess
import os
import glob
import shutil
import argparse

OUTPUT_DIR = "/Users/mokrzesik/Desktop/Michael/Music/Youtube/Marching Illini"
TEMP_DIR = os.path.join(os.getcwd(), "yt_temp")

def prompt_rename(original_title: str) -> str:
    print(f'\n📝 Current filename: "{original_title}"')
    new_name = input("Enter new name (or leave blank to keep original): ").strip()
    return new_name if new_name else original_title

def get_title(url: str) -> str:
    print("🔍 Fetching title...")
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def try_direct_download(url: str, audio_format: str) -> bool:
    """
    Try to produce the target format in one step via yt-dlp:
      - m4a:     bestaudio[ext=m4a] (no re-encode if available)
      - mp3:     extract & convert with ffmpeg via yt-dlp
    """
    if audio_format == "m4a":
        print("🎯 Attempting direct download as .m4a...")
        title = get_title(url)
        final_name = prompt_rename(title)
        output_path = os.path.join(OUTPUT_DIR, f"{final_name}.m4a")

        # Prefer native m4a if available
        result = subprocess.run([
            "yt-dlp",
            "-f", "bestaudio[ext=m4a]",
            "-o", output_path,
            url
        ])
        return result.returncode == 0

    elif audio_format == "mp3":
        print("🎯 Attempting direct download and conversion to .mp3 (yt-dlp postprocess)...")
        title = get_title(url)
        final_name = prompt_rename(title)
        output_path = os.path.join(OUTPUT_DIR, f"{final_name}.mp3")

        # Let yt-dlp extract and convert using ffmpeg
        result = subprocess.run([
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "--audio-quality", "192K",
            "-o", output_path,
            url
        ])
        return result.returncode == 0

    else:
        print(f"❌ Unsupported format: {audio_format}")
        return False

def fallback_download_and_convert(url: str, audio_format: str) -> None:
    print("⬇️ Direct approach failed, using fallback with manual conversion...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 1) Grab best available audio
    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-o", os.path.join(TEMP_DIR, "%(title)s.%(ext)s"),
        url
    ], check=True)

    # 2) Find the newest fetched file
    audio_files = glob.glob(os.path.join(TEMP_DIR, "*.*"))
    if not audio_files:
        print("❌ No audio file found for conversion.")
        return

    input_file = max(audio_files, key=os.path.getctime)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    final_name = prompt_rename(base_name)

    if audio_format == "m4a":
        output_file = os.path.join(OUTPUT_DIR, final_name + ".m4a")
        print(f"🔁 Converting {input_file} → {output_file} (AAC 192k)...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_file,
            "-c:a", "aac", "-b:a", "192k",
            output_file
        ], check=True)

    elif audio_format == "mp3":
        output_file = os.path.join(OUTPUT_DIR, final_name + ".mp3")
        print(f"🔁 Converting {input_file} → {output_file} (MP3 192k)...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_file,
            "-codec:a", "libmp3lame", "-b:a", "192k",
            output_file
        ], check=True)
    else:
        print(f"❌ Unsupported format in fallback: {audio_format}")
        return

    # 3) Cleanup temp
    try:
        os.remove(input_file)
    except OSError:
        pass
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print(f"✅ Done! Saved to: {output_file}")

def update_yt_dlp():
    print("🔄 Updating yt-dlp to the latest version...")
    subprocess.run(["brew", "upgrade", "yt-dlp"], check=True)
    print("✅ yt-dlp updated.")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube audio as MP3 or M4A."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    # Support the exact flags you asked for, plus long forms
    group.add_argument("-mp3", "--mp3", dest="format", action="store_const", const="mp3",
                       help="Download/convert to MP3")
    group.add_argument("-m4a", "--m4a", dest="format", action="store_const", const="m4a",
                       help="Download/convert to M4A")
    parser.add_argument("url", help="YouTube URL")
    return parser.parse_args()

def main():
    args = parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    url = args.url
    audio_format = args.format  # 'mp3' or 'm4a'

    update_yt_dlp()

    ok = try_direct_download(url, audio_format)
    if not ok:
        fallback_download_and_convert(url, audio_format)

if __name__ == "__main__":
    main()