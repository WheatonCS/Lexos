$ErrorActionPreference = 'Inquire'
Start-Process -FilePath 'cmd.exe' -ArgumentList '/k echo python is warmming up, we will start the browser for you when it is finished && echo please sit back and relax && echo. && echo if you want to close Lexos, just close this window && .\Anaconda2\python.exe C:\Lexos-master\lexos.py >nul 2>&1' -WorkingDirectory $HOME

Write-Host "python is warmming up, we will start the browser for you when it is finished" -ForegroundColor Cyan
Write-Host "please sit back and relax" -ForegroundColor Cyan

$webclient = New-Object net.webclient 
while($true){
    Write-Host '' 
    try{
        Write-Host 'see if Lexos is ready' 
        $trash = $webclient.OpenRead('http://localhost:5000'); 
        Write-Host 'Lexos is ready' -ForegroundColor Green
        break
    } 
    catch {
        Write-Host 'Lexos is still warming up' -ForegroundColor Yellow
    }
}

Start "http://localhost:5000"