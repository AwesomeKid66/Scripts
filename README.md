# 🧰 Utility Script Collection

A personal toolkit of **PowerShell** and **Python** scripts for automating common tasks — including managing iPhone photo folders, organizing media, and downloading YouTube videos and audio.

---

## 📁 Contents

| Script | Language | Description |
|--------|-----------|-------------|
| `rename_iphone_folders.ps1` | PowerShell | Consolidates and renames iPhone photo folders by year and month. |
| `sort_iphone_photos_videos.ps1` | PowerShell | Separates iPhone photos and videos into dedicated folders. |
| `disable-wake.ps1` | PowerShell | Disables all wake-enabled devices except the power button. |
| `download_video.py` | Python | Downloads a single YouTube video as `.mp4`. |
| `download_audio.py` | Python | Downloads or converts a single YouTube video into `.m4a` audio. |
| `download_playlist.py` | Python | Downloads all videos from a YouTube playlist as `.m4a` audio files. |

---

## ⚡ PowerShell Scripts

### 🗂️ 1. `rename_iphone_folders.ps1`

**Purpose:**
Consolidates iPhone backup folders into cleanly named `yyyy-mm` folders and merges all files accordingly.

**Behavior:**
- Scans the specified root directory for folders matching `yyyymm_` or `yyyymm__a` patterns.
- Renames them into `yyyy-mm` format (e.g., `202312__a` → `2023-12`).
- Moves all contained files into the new folder.
- Automatically appends `_1`, `_2`, etc., to duplicate filenames.
- Deletes old folders once files have been moved.

**Usage:**
```powershell
# Edit the root folder path at the top of the script:
$rootFolder = "D:\Pictures\IPhone pictures"

# Then run:
.\rename_iphone_folders.ps1
