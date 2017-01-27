@echo off
cmd /C "cd C:\ && powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/WheatonCS/Lexos/master/install/Windows/config.ps1'))""
