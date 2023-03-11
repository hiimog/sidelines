# user is windex2302eval\user
# needs to run as admin
$ErrorActionPreference = "Stop"
set-executionpolicy -scope localmachine unrestricted
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://vcredist.com/install.ps1'))
Set-TimeZone -Id "Eastern Standard Time"
choco feature enable -n allowGlobalConfirmation
choco install `
	7zip `
	bat `
	cmake `
	curl `
	delta `
	git `
	gnuwin32-coreutils.install `
	googlechrome `
	jetbrainstoolbox `
	linqpad7.install `
	microsoft-windows-terminal --pre `
	mingw `
	neovim `
	nodejs `
	python3 `
	rustup.install `
	seq `
	vscode `
	wget
