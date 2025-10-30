import subprocess
import sys
import os

OUTPUT_DIR = "/Users/mokrzesik/Desktop/Michael/Music/Youtube/Marching Illini"

def prompt_rename(original_title):
    print(f'\n🎬 Current video title: "{original_title}"')
    new_name = input("Enter new name (or leave blank to keep original): ").strip()
    return new_name if new_name else original_title

def get_video_title(url):
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def download_video(url, final_filename):
    output_path = os.path.join(OUTPUT_DIR, f"{final_filename}.mp4")

    print(f"⬇️ Downloading and saving to: {output_path}")
    subprocess.run([
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url
    ], check=True)

    print(f"✅ Done! Video saved to: {output_path}")

def update_yt_dlp():
    print("🔄 Updating yt-dlp to the latest version...")
    subprocess.run(["yt-dlp", "-U"], check=True)
    print("✅ yt-dlp updated.")

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run download_video.py [YouTube_URL]")
        sys.exit(1)

    url = sys.argv[1]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    update_yt_dlp()

    try:
        title = get_video_title(url)
        final_name = prompt_rename(title)
        download_video(url, final_name)
    except subprocess.CalledProcessError as e:
        print("❌ An error occurred during download or merging.")
        print(e)

if __name__ == "__main__":
    main()
