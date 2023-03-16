function goeng {
    Set-Location C:\src\sidelines\eng
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

function goroot {
    Set-Location c:\src\sidelines
}

function l {
    Param (
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]
        $TheRest
    )
    Get-ChildItem @TheRest
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

Remove-Item alias:wget 


