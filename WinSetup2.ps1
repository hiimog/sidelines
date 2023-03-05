$ErrorActionPreference = "Stop"
# does not need admin
$ghtoken = read-host "Enter github token: "
$ghtoken > ~/.github
	
mkdir C:\src
mkdir C:\tools
cd C:\tools
git clone https://github.com/Microsoft/vcpkg.git C:\tools\vcpkg
iex c:\tools\vcpkg\bootstrap-vcpkg.bat

read-host "Start installation of Clion"

cd c:\src
git clone https://github.com/hiimog/sidelines.git