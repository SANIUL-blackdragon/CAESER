function Show-Tree {
    param (
        [string]$Path = ".",
        [string]$Indent = "",
        [string[]]$Exclude = @('venv', 'node_modules', '.git', '.vscode', 'dist', 'build', '__pycache__', '__MACOSX', '.DS_Store')
    )

    # Get all items (directories and files), excluding specified directories
    $items = Get-ChildItem -Path $Path | Where-Object { $_.PSIsContainer -or $Exclude -notcontains $_.Name }
    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            # Directory
            if ($Exclude -notcontains $item.Name) {
                Write-Output "$Indent+-- $($item.Name)/"
                Show-Tree -Path $item.FullName -Indent "$Indent|   " -Exclude $Exclude
            }
        } else {
            # File
            Write-Output "$Indent|-- $($item.Name)"
        }
    }
}

# Run the function
Show-Tree