@echo off
cmd /C "cd C:\ && powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://github.com/WheatonCS/Lexos/blob/master/install/Windows/update.ps1'))""
