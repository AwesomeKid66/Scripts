# Set your root folder where all the iPhone photos and videos are
$rootFolder = "D:\Pictures\IPhone pictures"

# Get all directories in the root folder
$folders = Get-ChildItem -Path $rootFolder -Directory

foreach ($folder in $folders) {
    # Match the pattern yyyymm_ and optionally a letter
    if ($folder.Name -match '^(\d{4})(\d{2})__?([a-z]?)$') {
        $year = $matches[1]
        $month = $matches[2]

        # Convert to mm-yyyy format
        $newFolderName = "{0}-{1}" -f $year, $month
        $newFolderPath = Join-Path $rootFolder $newFolderName

        # Create the new folder if it doesn't exist
        if (-not (Test-Path $newFolderPath)) {
            New-Item -Path $newFolderPath -ItemType Directory | Out-Null
        }

        # Move all files from the current folder into the new folder
        Get-ChildItem -Path $folder.FullName -File | ForEach-Object {
            $destination = Join-Path $newFolderPath $_.Name
            # Handle duplicate file names by appending a number
            $counter = 1
            while (Test-Path $destination) {
                $baseName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
                $ext = [System.IO.Path]::GetExtension($_.Name)
                $destination = Join-Path $newFolderPath ("{0}_{1}{2}" -f $baseName, $counter, $ext)
                $counter++
            }
            Move-Item -Path $_.FullName -Destination $destination
        }

        # Remove the old folder after moving files
        Remove-Item -Path $folder.FullName -Recurse
    }
}

Write-Host "Folders have been consolidated and renamed."
