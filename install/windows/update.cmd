@echo off
cmd /C "powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/WheatonCS/Lexos/master/install/windows/update.ps1'))""
