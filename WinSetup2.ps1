$ErrorActionPreference = "Stop"
# does not need admin
$ghtoken = read-host "Enter github token: "
$ghtoken > ~/.github
	
mkdir C:\src
mkdir C:\tools
Set-Location C:\tools
git clone https://github.com/Microsoft/vcpkg.git C:\tools\vcpkg
Invoke-Expression c:\tools\vcpkg\bootstrap-vcpkg.bat
[System.Environment]::SetEnvironmentVariable('Path', "${env:Path};c:\tools\vcpkg", 'User')

read-host "Start installation of Clion"

Set-Location c:\src
git clone https://github.com/hiimog/sidelines.git

Copy-Item .\WinDevProfile.ps1 C:\Users\User\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1