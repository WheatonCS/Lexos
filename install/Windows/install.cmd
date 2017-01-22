@echo off
set "location=%CD%"
cd %temp%
@powershell -NoProfile -ExecutionPolicy Bypass -Command "(new-object net.webclient).DownloadFile('https://raw.githubusercontent.com/WheatonCS/Lexos/v3.0/install/Windows/install.ps1', './install.ps1'); & './install.ps1'  %*"
cd %location%
