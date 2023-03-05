function gocli {
    Set-Location C:\src\sidelines\cli
}

function goutil {
    Set-Location C:\src\sidelines\util
}

function goapp {
    Set-Location C:\src\sidelines\app
}

function gotemp {
    Set-Location c:\temp
}

function mkcd {
    param (
        [string] $Dir
    )
    $existing = Get-Item $Dir -ErrorAction Ignore
    if (-Not $existing) {
        mkdir $Dir
    }
    set-location $Dir
}

function copyguid {
    Set-Clipboard -Value ([guid]::NewGuid().ToString())
}