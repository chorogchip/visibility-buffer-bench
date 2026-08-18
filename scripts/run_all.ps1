$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& python.exe (Join-Path $ScriptDir "reproduce.py") --suite all @args
exit $LASTEXITCODE
