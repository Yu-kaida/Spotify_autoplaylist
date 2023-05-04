@echo off
if "%-1" == "" (
    echo Usage: setup.bat <env_file_path> <client_id> <client_secret>
    exit /b 1
)

set ENV_FILE=%~1
set CLIENT_ID=%2
set CLIENT_SECRET=%3

echo CLIENT_ID=%CLIENT_ID% > %ENV_FILE%
echo CLIENT_SECRET=%CLIENT_SECRET% >> %ENV_FILE%

echo Environment file created at %ENV_FILE%
```