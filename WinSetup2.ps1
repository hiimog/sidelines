$ErrorActionPreference = "Stop"
# does not need admin
$ghtoken = read-host "Enter github token: "
$ghtoken > ~/.github
	
mkdir C:\src
mkdir C:\tools
cd C:\tools
git clone https://github.com/Microsoft/vcpkg.git C:\tools\vcpkg
iex c:\tools\vcpkg\bootstrap-vcpkg.bat
[System.Environment]::SetEnvironmentVariable('Path', "${env:Path};c:\tools\vcpkg", 'User')

read-host "Start installation of Clion"

cd c:\src
git clone https://github.com/hiimog/sidelines.git

cp .\WinDevProfile.ps1 C:\Users\User\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1