<#
.SYNOPSIS
Enhanced Project Dumper 9000™ with Database File Handling

.DESCRIPTION
This script generates a markdown summary of a project, excluding specified directories and files.

.NOTES
Run this script in PowerShell. Example:
    .\ProjectDumper.ps1 -OutputPath "docs/summary.md"
#>
param(
    [string]$OutputPath = "docs/md/summary-of-alpha.md",
    [string[]]$ExcludeDirs = @(".git", "venv", "node_modules", ".vscode", "__pycache__", "test", "tests", "__tests__", "spec", "config", "configs", "configuration", "settings"),
    [string[]]$ExcludeFiles = @("\.log$", "\.tmp$", "\.exe$", "\.dll$", "\.bin$", "\.txt$", "\.config$", "\.conf$", "\.cfg$", "\.ini$", "\.settings$", "\.bak$", "\.swp$", "\.swo$", "\.old$", "\.orig$", "\.patch$", "\.diff$", "\.md5$", "\.sha1$", "\.sha256$", "\.json$", "\.mjs$", "\.cjs$", "\.tsbuildinfo$", "\.d\.ts$", "\.map$", "\.lock$", "\.zip$", "\.tar$", "\.gz$", "\.rar$", "\.7z$"),
    # New parameter for database file extensions
    [string[]]$DatabaseExtensions = @(".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"),
    [int]$MaxFileSize = 10MB,
    [switch]$IncludeBinary
)

$basePath = Get-Location
$stats = @{
    TotalFiles = 0
    ProcessedFiles = 0
    SkippedFiles = 0
    BinaryFiles = 0
    DatabaseFiles = 0  # New category for tracking database files
    LargeFiles = 0
}

# Function to check if file is a database file
function Test-DatabaseFile {
    param([System.IO.FileInfo]$File)
    
    $extension = $File.Extension.ToLower()
    return $DatabaseExtensions -contains $extension
}

# Ensure target directory exists
New-Item -ItemType Directory -Force -Path (Split-Path $OutputPath) | Out-Null

# Create header with timestamp and parameters
$header = @"
# Project Dump of $($basePath)

**Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Max File Size:** $([math]::Round($MaxFileSize / 1MB, 2))MB
**Excluded Directories:** $($ExcludeDirs -join ', ')
**Excluded Files:** $($ExcludeFiles -join ', ')
**Database Extensions:** $($DatabaseExtensions -join ', ')

---

"@

Set-Content -Path $OutputPath -Value $header

Write-Host "🚀 Starting Project Dumper 9000™..." -ForegroundColor Green
Write-Host "📁 Base Path: $basePath" -ForegroundColor Cyan
Write-Host "📄 Output: $OutputPath" -ForegroundColor Cyan

# Get all files with filtering (same as before)
$allFiles = Get-ChildItem -Path $basePath -Recurse -File -Force | Where-Object {
    $fullPath = $_.FullName
    $relativePath = $_.FullName.Substring($basePath.Path.Length + 1)
    
    # Check directory exclusions
    $dirPath = $_.DirectoryName
    $dirParts = $dirPath -split '\\'
    $excludeDir = $false
    foreach ($part in $dirParts) {
        if ($ExcludeDirs -contains $part) {
            $excludeDir = $true
            break
        }
    }
    
    # Check file exclusions
    $excludeFile = $false
    foreach ($pattern in $ExcludeFiles) {
        if ($relativePath -match $pattern) {
            $excludeFile = $true
            break
        }
    }
    
    return (-not ($excludeDir -or $excludeFile))
}

$stats.TotalFiles = $allFiles.Count
Write-Host "📊 Found $($stats.TotalFiles) files to process" -ForegroundColor Yellow

$i = 0
foreach ($file in $allFiles) {
    $i++
    $relativePath = $file.FullName.Substring($basePath.Path.Length + 1)
    
    # Progress indicator
    if ($i % 10 -eq 0 -or $i -eq $stats.TotalFiles) {
        $percent = [math]::Round(($i / $stats.TotalFiles) * 100, 1)
        $statusMessage = '{0} of {1} ({2:F1}%)' -f $i, $stats.TotalFiles, $percent
        Write-Progress -Activity "Processing files" -Status $statusMessage -PercentComplete $percent
    }
    
    # Always add the file header to show it exists in the tree
    $fileHeader = "`n---`n### File: $relativePath"
    Add-Content -Path $OutputPath -Value $fileHeader
    
    # Check if this is a database file FIRST (before size/binary checks)
    if (Test-DatabaseFile -File $file) {
        # Database files: show in tree but don't dump contents
        $dbInfo = "_[Database file - $([math]::Round($file.Length / 1KB, 1))KB]_"
        Add-Content -Path $OutputPath -Value $dbInfo
        $stats.DatabaseFiles++
        $stats.SkippedFiles++
        continue  # Skip to next file - don't process contents
    }
    
    # Check file size (for non-database files)
    if ($file.Length -gt $MaxFileSize) {
        $sizeMessage = "_[File too large: $([math]::Round($file.Length / 1MB, 2))MB]_"
        Add-Content -Path $OutputPath -Value $sizeMessage
        $stats.LargeFiles++
        $stats.SkippedFiles++
        continue
    }
    
    # Check if binary (simple heuristic) - only for non-database files
    $isBinary = $false
    if (-not $IncludeBinary) {
        try {
            $sample = Get-Content -Path $file.FullName -TotalCount 1 -Encoding Byte -ErrorAction Stop
            if ($sample -and ($sample | Where-Object { $_ -eq 0 -or $_ -gt 127 }).Count -gt 0) {
                $isBinary = $true
            }
        }
        catch {
            # If we can't read it, assume it's binary
            $isBinary = $true
        }
    }
    
    if ($isBinary) {
        Add-Content -Path $OutputPath -Value "_[Binary file - $($file.Length) bytes]_"
        $stats.BinaryFiles++
        $stats.SkippedFiles++
    }
    else {
        try {
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop
            
            # Detect file type for syntax highlighting
            $extension = $file.Extension.ToLower()
            $language = switch ($extension) {
                '.ps1' { 'powershell' }
                '.py' { 'python' }
                '.js' { 'javascript' }
                '.ts' { 'typescript' }
                '.html' { 'html' }
                '.css' { 'css' }
                '.xml' { 'xml' }
                '.yml' { 'yaml' }
                '.yaml' { 'yaml' }
                '.md' { 'markdown' }
                '.sh' { 'bash' }
                '.sql' { 'sql' }
                '.cs' { 'csharp' }
                '.cpp' { 'cpp' }
                '.c' { 'c' }
                '.java' { 'java' }
                default { 'text' }
            }
            
            $codeBlock = "````````$language
`n$content`n``````"
            Add-Content -Path $OutputPath -Value $codeBlock
            $stats.ProcessedFiles++
        }
        catch {
            Add-Content -Path $OutputPath -Value "_[Could not read file: $($_.Exception.Message)]_"
            $stats.SkippedFiles++
        }
    }
}

Write-Progress -Activity "Processing files" -Completed

# Enhanced summary statistics that include database file tracking
$summaryStats = @"
`n`n---`n`n## Summary Statistics
- **Total Files Found:** $($stats.TotalFiles)
- **Successfully Processed:** $($stats.ProcessedFiles)
- **Skipped (Database Files):** $($stats.DatabaseFiles)
- **Skipped (Binary):** $($stats.BinaryFiles)
- **Skipped (Too Large):** $($stats.LargeFiles)
- **Skipped (Errors):** $($stats.SkippedFiles - $stats.BinaryFiles - $stats.LargeFiles - $stats.DatabaseFiles)
- **Total Skipped:** $($stats.SkippedFiles)

**Completion:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@ 

Add-Content -Path $OutputPath -Value $summaryStats

Write-Host ""
Write-Host "✅ Project dump completed!" -ForegroundColor Green
Write-Host "📄 Output saved to: $OutputPath" -ForegroundColor Cyan
Write-Host "📊 Processed: $($stats.ProcessedFiles)/$($stats.TotalFiles) files" -ForegroundColor Yellow
Write-Host "🗄️  Database files found: $($stats.DatabaseFiles)" -ForegroundColor Magenta