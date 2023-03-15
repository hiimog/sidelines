$ErrorActionPreference = "Stop"
# does not need admin
pip install `
    click `
    chess `
    mako `
    orjson `
    pytest `
    seqlog

#needs admin
pip install --editable C:\src\sidelines\cli
mkdir C:\Users\User\AppData\Local\nvim

# link win dev profile to location
set-location ~/Documents/WindowsPowerShell/; new-item -type SymbolicLink . -Name Microsoft.PowerShell_profile.ps1 -Value C:\src\sidelines\WinDevProfile.ps1