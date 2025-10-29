# Set your root folder containing yyyy-mm folders
$rootFolder = "D:\Pictures\IPhone pictures RAW name"

# Set your destination folders
$photoDest = "D:\Pictures\IPhone pictures"
$videoDest = "D:\Pictures\IPhone videos"

# Define file extensions for pictures and videos
$pictureExtensions = ".jpg", ".jpeg", ".png", ".heic", ".bmp", ".gif", ".tiff", ".webp", ".dng"
$videoExtensions   = ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"

# Get all yyyy-mm folders in the root folder
$folders = Get-ChildItem -Path $rootFolder -Directory

foreach ($folder in $folders) {

    # Initialize lists to track files
    $photoFiles = @()
    $videoFiles = @()

    # Get all files in the current folder
    $files = Get-ChildItem -Path $folder.FullName -File

    foreach ($file in $files) {
        $ext = $file.Extension.ToLower()
        if ($ext -eq ".aae") {
            # Delete .aae files
            Remove-Item -Path $file.FullName -Force
            Write-Host "Deleted .aae file: $($file.FullName)"
        }
        elseif ($pictureExtensions -contains $ext) {
            $photoFiles += $file
        }
        elseif ($videoExtensions -contains $ext) {
            $videoFiles += $file
        }
    }

    # Move photo files if any
    if ($photoFiles.Count -gt 0) {
        $photoFolder = Join-Path $photoDest $folder.Name
        if (-not (Test-Path $photoFolder)) { New-Item -Path $photoFolder -ItemType Directory | Out-Null }
        foreach ($file in $photoFiles) {
            Move-Item -Path $file.FullName -Destination (Join-Path $photoFolder $file.Name)
        }
    }

    # Move video files if any
    if ($videoFiles.Count -gt 0) {
        $videoFolder = Join-Path $videoDest $folder.Name
        if (-not (Test-Path $videoFolder)) { New-Item -Path $videoFolder -ItemType Directory | Out-Null }
        foreach ($file in $videoFiles) {
            Move-Item -Path $file.FullName -Destination (Join-Path $videoFolder $file.Name)
        }
    }

    # Optional: remove the original folder if empty
    if ((Get-ChildItem -Path $folder.FullName -Recurse | Measure-Object).Count -eq 0) {
        Remove-Item -Path $folder.FullName
    }
}

Write-Host "Files have been sorted into Photos and Videos destinations, .aae files deleted, and empty folders skipped."
