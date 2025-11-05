# Utility Scripts Collection

A collection of PowerShell and Python scripts for managing media files, downloading YouTube content, and system configuration.

## Table of Contents

- [PowerShell Scripts](#powershell-scripts)
  - [iPhone Photo Folder Converter](#iphone-photo-folder-converter)
  - [Photo/Video Splitter](#photovideo-splitter)
  - [Disable Wake Devices](#disable-wake-devices)
- [Python Scripts](#python-scripts)
  - [YouTube Audio Downloader](#youtube-audio-downloader)
  - [YouTube Playlist Downloader](#youtube-playlist-downloader)
  - [YouTube Video Downloader](#youtube-video-downloader)

---

## PowerShell Scripts

### iPhone Photo Folder Converter

**File:** `convert_iphone_folders_naming.ps1`

Consolidates and renames iPhone photo folders from the format `yyyymm_` (with optional letter suffix) to `yyyy-mm`.

**Features:**
- Converts folder names from `202301_`, `202301a`, `202301_a` → `2023-01`
- Merges files from multiple source folders into consolidated month folders
- Handles duplicate filenames by appending numbers
- Removes empty source folders after migration

**Usage:**
```powershell
# Edit the script to set your root folder path
$rootFolder = "D:\Pictures\IPhone pictures"

# Run the script
.\convert_iphone_folders_naming.ps1
```

---

### Photo/Video Splitter

**File:** `split_photo_video.ps1`

Organizes mixed media files by separating photos and videos into different directory structures while maintaining month-based organization.

**Features:**
- Separates photos and videos from mixed folders
- Maintains `yyyy-mm` folder structure in both destinations
- Deletes `.aae` (Apple metadata) files automatically
- Removes empty source folders after processing

**Supported Formats:**
- **Photos:** `.jpg`, `.jpeg`, `.png`, `.heic`, `.bmp`, `.gif`, `.tiff`, `.webp`, `.dng`
- **Videos:** `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`

**Usage:**
```powershell
# Edit the script to set your paths
$rootFolder = "D:\Pictures\IPhone pictures RAW name"
$photoDest = "D:\Pictures\IPhone pictures"
$videoDest = "D:\Pictures\IPhone videos"

# Run the script
.\split_photo_video.ps1
```

---

### Disable Wake Devices

**File:** `remove_power_awake_devices.ps1`

Disables all devices that can wake your computer from sleep, except the power button.

**Features:**
- Self-elevates to administrator privileges
- Lists all wake-enabled devices before disabling
- Keeps PowerShell window open to show results
- Useful for preventing accidental wake from mouse/keyboard

**Usage:**
```powershell
# Simply run the script - it will request admin privileges automatically
.\remove_power_awake_devices.ps1
```

---

## Python Scripts

### Prerequisites

All Python scripts require:
- Python 3.7+
- `yt-dlp` installed (`pip install yt-dlp`)
- `ffmpeg` installed and in system PATH

### YouTube Audio Downloader

**File:** `download_youtube_audio.py`

Downloads audio from a single YouTube video in MP3 or M4A format.

**Features:**
- Downloads audio at 192kbps quality
- Interactive filename renaming
- Automatic yt-dlp updates before download
- Fallback conversion using ffmpeg if direct download fails

**Usage:**
```bash
# Download as MP3
./download_youtube_audio.py -mp3 "https://www.youtube.com/watch?v=VIDEO_ID"

# Download as M4A
./download_youtube_audio.py -m4a "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Default Output Location:**
```
/Users/mokrzesik/Desktop/Michael/Music/Youtube/Marching Illini
```

Edit the `OUTPUT_DIR` variable in the script to change the destination.

---

### YouTube Playlist Downloader

**File:** `download_youtube_playlist.py`

Downloads audio from entire YouTube playlists or individual videos.

**Features:**
- Processes entire playlists automatically
- Works with single videos too
- Interactive renaming for each track
- Custom output directory support
- Continues on error (won't stop if one video fails)

**Usage:**
```bash
# Download playlist as MP3
./download_youtube_playlist.py -mp3 "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Download playlist as M4A with custom output
./download_youtube_playlist.py -m4a "PLAYLIST_URL" --output-dir "/path/to/folder"

# Works with single videos too
./download_youtube_playlist.py -mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Default Output Location:**
```
/Users/mokrzesik/Desktop/Michael/Music/Youtube
```

---

### YouTube Video Downloader

**File:** `download_youtube_video.py`

Downloads YouTube videos with various format and quality options.

**Features:**
- Multiple container formats: MP4, WEBM, MKV
- Quality control with `--max-height` option
- Interactive title renaming
- Automatic stream merging (video + audio)

**Formats:**
- **MP4:** H.264 video + AAC audio
- **WEBM:** VP9 video + Opus audio
- **MKV:** Any available codecs (most flexible)

**Usage:**
```bash
# Download as MP4
./download_youtube_video.py -mp4 "https://www.youtube.com/watch?v=VIDEO_ID"

# Download as WEBM with max 1080p quality
./download_youtube_video.py -webm "VIDEO_URL" --max-height 1080

# Download as MKV with custom output directory
./download_youtube_video.py -mkv "VIDEO_URL" --output-dir "/path/to/videos"

# Limit to 720p
./download_youtube_video.py -mp4 "VIDEO_URL" --max-height 720
```

**Default Output Location:**
```
/Users/mokrzesik/Desktop/Michael/Music/Youtube/Videos/Marching Illini
```

---

## Installation

### PowerShell Scripts

1. Clone this repository
2. Edit file paths in scripts to match your system
3. Run scripts in PowerShell (some may require administrator privileges)

### Python Scripts

1. Clone this repository
2. Install dependencies:
```bash
   pip install yt-dlp
```
3. Install ffmpeg:
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org)
4. Make scripts executable (Unix-based systems):
```bash
   chmod +x *.py
```
5. Edit `OUTPUT_DIR` variables in scripts to match your desired locations

---

## License

These scripts are provided as-is for personal use. Feel free to modify and distribute.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
