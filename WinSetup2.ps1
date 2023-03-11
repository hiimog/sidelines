$ErrorActionPreference = "Stop"
# does not need admin
$ghtoken = read-host "Enter github token: "
$ghtoken > ~/.github

# needs admin
npm i -g http-server prettier yarn
cargo install tauri-cli

mkdir C:\src
mkdir C:\tools
Set-Location C:\tools
git clone https://github.com/Microsoft/vcpkg.git C:\tools\vcpkg
Invoke-Expression c:\tools\vcpkg\bootstrap-vcpkg.bat
[System.Environment]::SetEnvironmentVariable('Path', "${env:Path};c:\tools\vcpkg", 'User')

read-host "Start installation of Clion"

# should be done unelevated
Set-Location c:\src
git clone https://github.com/hiimog/sidelines.git

# this should be linked
Copy-Item .\WinDevProfile.ps1 C:\Users\User\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1

# unelevated 
# requires host changes for the vm: Set-VMProcessor -VMName 'Name of the VM this is for' -ExposeVirtualizationExtensions $True
Invoke-Expression wsl --install -d Ubuntu-22.04