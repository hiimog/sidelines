# user is windex2302eval\user
$ErrorActionPreference = "Stop"
set-executionpolicy -scope localmachine unrestricted
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://vcredist.com/install.ps1'))
choco feature enable -n allowGlobalConfirmation
choco install `
	7zip `
	cmake `
	curl `
	git `
	gnuwin32-coreutils.install `
	googlechrome `
	jetbrainstoolbox `
	microsoft-windows-terminal --pre `
	mingw `
	python3 `
	rustup.install `
	vscode 
