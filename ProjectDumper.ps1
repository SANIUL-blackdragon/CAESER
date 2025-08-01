#
# Simplified Project Dumper - Clean Version
# Just copies files once with clear headers, ignoring what you specify
#
param(
    [string]$OutputPath = "project-dump.md",
    [string[]]$ExcludeDirs = @(".git", "venv", "node_modules", ".vscode", "__pycache__", "test", "tests", "config", "node_modules", "dist", "build", "logs", "temp", "tmp", "cache", "txt", "img", "md"),
    [string[]]$ExcludeFiles = @("*.log", "*.tmp", "*.exe", "*.dll", "*.bin", "*.zip", "*.tar", "*.gz", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.pdf", ".json", ".lock", ".md", ".ldf", ".bak", ".ps1",  ".db", "mjs", "package-lock.json" ,"package.json", "ProjectDumper - Copy.ps1", "ProjectDumper.ps1", ".env"),
    [int]$MaxFileSize = 10MB
)

$basePath = Get-Location
$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

# Create header
$header = @"
# Project Dump: $basePath
Generated: $timestamp
Max File Size: $([math]::Round($MaxFileSize / 1MB, 2))MB

---

"@

# Write header to file
Set-Content -Path $OutputPath -Value $header -Encoding UTF8

Write-Host "Scanning files..." -ForegroundColor Yellow

# Get all files, excluding what we don't want
$allFiles = Get-ChildItem -Path $basePath -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {
    $relativePath = $_.FullName.Substring($basePath.Path.Length + 1)
    
    # Skip excluded directories
    $skipDir = $false
    foreach ($dir in $ExcludeDirs) {
        if ($relativePath -like "*$dir*") {
            $skipDir = $true
            break
        }
    }
    
    # Skip excluded files
    $skipFile = $false
    foreach ($pattern in $ExcludeFiles) {
        if ($_.Name -like $pattern) {
            $skipFile = $true
            break
        }
    }
    
    # Skip if too large
    $tooLarge = $_.Length -gt $MaxFileSize
    
    return -not ($skipDir -or $skipFile -or $tooLarge)
}

Write-Host "Found $($allFiles.Count) files to process" -ForegroundColor Green

$processed = 0
foreach ($file in $allFiles) {
    $processed++
    $relativePath = $file.FullName.Substring($basePath.Path.Length + 1)
    
    Write-Progress -Activity "Processing" -Status $relativePath -PercentComplete (($processed / $allFiles.Count) * 100)
    
    try {
        # Get file extension for syntax highlighting
        $ext = $file.Extension.ToLower()
        $language = switch ($ext) {
            ".ps1" { "powershell" }
            ".py" { "python" }
            ".js" { "javascript" }
            ".ts" { "typescript" }
            ".html" { "html" }
            ".css" { "css" }
            ".xml" { "xml" }
            ".yml" { "yaml" }
            ".yaml" { "yaml" }
            ".md" { "markdown" }
            ".sh" { "bash" }
            ".sql" { "sql" }
            ".cs" { "csharp" }
            ".cpp" { "cpp" }
            ".c" { "c" }
            ".java" { "java" }
            ".json" { "json" }
            default { "text" }
        }
        
        # Read file content
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8 -ErrorAction Stop
        
        if ([string]::IsNullOrEmpty($content)) {
            $content = "[Empty file]"
        }
        
        # Build the output for this file
        $fileOutput = @"

## File: $relativePath

`````$language

$content
```

"@
        
        # Append to output file
        Add-Content -Path $OutputPath -Value $fileOutput -Encoding UTF8
        
    }
    catch {
        # Handle files that can't be read
        $errorOutput = @"

## File: $relativePath
[Error reading file: $($_.Exception.Message)]

"@
        Add-Content -Path $OutputPath -Value $errorOutput -Encoding UTF8
    }
}

Write-Progress -Activity "Processing" -Completed

# Add summary
$summary = @"

---
## Summary
Total files processed: $processed
Completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@

Add-Content -Path $OutputPath -Value $summary -Encoding UTF8

Write-Host "Done! Output saved to: $OutputPath" -ForegroundColor Green
Write-Host "Processed $processed files" -ForegroundColor Cyan