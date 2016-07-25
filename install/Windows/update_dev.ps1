$ErrorActionPreference = 'Inquire'
$location = Get-Location

Set-Location $HOME/AppData/Local/Temp/
$curLocation = Get-Location

# downloading lexos
Write-Host ' '
Write-Host 'downloading lexos' -ForegroundColor Green

Write-Host 'This could take a while...' -ForegroundColor Green
Write-Host 'Sorry we cannot display the status of the download, because it slows down the download' -ForegroundColor Green
Write-Host 'Please sit back and relax' -ForegroundColor Green
$lexosUrl = 'https://github.com/WheatonCS/Lexos/archive/master.zip'
(new-object net.webclient).DownloadFile($lexosUrl, "$curLocation/master.zip")


# installing lexos
Write-Host ' '
Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
if(Test-Path 'C:\Lexos-master'){
    Write-Host 'you already have lexos installed, removing the original install'
    Remove-Item C:\Lexos-master -Recurse -Force -Confirm:$false
    Write-Host ' '
    Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
    Expand-Archive -Path "$curLocation\master.zip" -DestinationPath "C:\"
    Write-Host 'your lexos is updated'
}
else {
    Write-Host "you don't seems to have lexos installed"
    Write-Host ' '
    Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
    Expand-Archive -Path "$curLocation\master.zip" -DestinationPath "C:\"
    Write-Host "we have successfully installed lexos for you."
}

# renew desktop icon
Write-Host 'We are recreating the desktop icons for you ^_^'
# run.cmd
$shell = New-Object -ComObject WScript.Shell
if(Test-Path "$desktop\Lexos.lnk") {Remove-Item -Force "$desktop\Lexos.lnk"}
$shortcut = $shell.CreateShortcut("$desktop\Lexos.lnk")
$shortcut.TargetPath = "C:\Lexos-master\install\windows\run.cmd"
$Shortcut.IconLocation = "C:\Lexos-master\install\assets\Lexos.ico"
$shortcut.Save()
# update.cmd
$shell = New-Object -ComObject WScript.Shell
if(Test-Path "$desktop\Lexos_Updater.lnk") {Remove-Item -Force "$desktop\Lexos_Updater.lnk"}
$shortcut = $shell.CreateShortcut("$desktop\Lexos_Updater.lnk")
$shortcut.TargetPath = "C:\Lexos-master\install\windows\run.cmd"
$Shortcut.IconLocation = "C:\Lexos-master\install\assets\Lexos_Update.ico"
$shortcut.Save()

# clean up
Remove-Item -Force -Confirm:$false 'master.zip'

# go back
Set-Location $location

Write-Host 'we have cleaned up' -ForegroundColor Green
Read-Host 'you can press enter to close this windows now'