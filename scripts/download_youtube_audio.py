import subprocess
import sys
import os
import glob
import shutil

OUTPUT_DIR = "/Users/mokrzesik/Desktop/Michael/Music/Youtube"
TEMP_DIR = os.path.join(os.getcwd(), "yt_temp")

def prompt_rename(original_title):
    print(f'\n📝 Current filename: "{original_title}"')
    new_name = input("Enter new name (or leave blank to keep original): ").strip()
    return new_name if new_name else original_title

def try_direct_m4a(url):
    print("🎯 Attempting direct download as .m4a...")

    # Use yt-dlp to get the title first
    print("🔍 Fetching title...")
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, check=True
    )
    title = result.stdout.strip()
    final_name = prompt_rename(title)
    output_path = os.path.join(OUTPUT_DIR, f"{final_name}.m4a")

    result = subprocess.run([
        "yt-dlp",
        "-f", "bestaudio[ext=m4a]",
        "-o", output_path,
        url
    ])
    return result.returncode == 0

def fallback_download_and_convert(url):
    print("⬇️ Direct download failed, using fallback with conversion...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-o", os.path.join(TEMP_DIR, "%(title)s.%(ext)s"),
        url
    ], check=True)

    audio_files = glob.glob(os.path.join(TEMP_DIR, "*.*"))
    if not audio_files:
        print("❌ No audio file found for conversion.")
        return

    input_file = max(audio_files, key=os.path.getctime)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    final_name = prompt_rename(base_name)
    output_file = os.path.join(OUTPUT_DIR, final_name + ".m4a")

    print(f"🔁 Converting {input_file} to {output_file}...")
    subprocess.run([
        "ffmpeg", "-i", input_file,
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ], check=True)

    os.remove(input_file)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print(f"✅ Done! Saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run script.py [YouTube_URL]")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    url = sys.argv[1]

    if not try_direct_m4a(url):
        fallback_download_and_convert(url)

if __name__ == "__main__":
    main()
