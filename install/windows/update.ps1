$ErrorActionPreference = 'Inquire'
$location = Get-Location

Set-Location $HOME/AppData/Local/Temp/
$curLocation = Get-Location

# load the config
Invoke-Expression (New-Object Net.Webclient).DownloadString('https://raw.githubusercontent.com/WheatonCS/Lexos/master/install/windows/config.ps1')

# downloading lexos
Write-Host ' '
Write-Host 'downloading lexos' -ForegroundColor Green

Write-Host 'This could take a while...' -ForegroundColor Green
Write-Host 'Sorry we cannot display the status of the download, because it slows down the download' -ForegroundColor Green
Write-Host 'Please sit back and relax' -ForegroundColor Green
(new-object net.webclient).DownloadFile($lexosZipUrl, "$curLocation/master.zip")


# installing lexos
Write-Host ' '
Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
if(Test-Path $lexosLocation){
    Write-Host 'you already have lexos installed, removing the original install'
    Remove-Item $lexosLocation -Recurse -Force -Confirm:$false
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

# creating desktop icon
Write-Host ' '
Write-Host 'creating desktop icon for you ^_^' -ForegroundColor Green
$desktop = [System.Environment]::GetFolderPath('Desktop')
# run.cmd
$shell = New-Object -ComObject WScript.Shell
if(Test-Path "$desktop\Lexos.lnk") {Remove-Item -Force "$desktop\Lexos.lnk"}
$shortcut = $shell.CreateShortcut("$desktop\Lexos.lnk")
$shortcut.TargetPath = "$lexosExecutableLocation\run.cmd"
$Shortcut.IconLocation = "$lexosAssets\Lexos.ico"
$shortcut.Save()
# update.cmd
$shell = New-Object -ComObject WScript.Shell
if(Test-Path "$desktop\Lexos_Updater.lnk") {Remove-Item -Force "$desktop\Lexos_Updater.lnk"}
$shortcut = $shell.CreateShortcut("$desktop\Lexos_Updater.lnk")
$shortcut.TargetPath = "$lexosExecutableLocation\update.cmd"
$Shortcut.IconLocation = "$lexosAssets\Lexos_Update.ico"
$shortcut.Save()

# clean up
Remove-Item -Force -Confirm:$false 'master.zip'

# go back
Set-Location $location

Write-Host 'we have cleaned up' -ForegroundColor Green
Read-Host 'you can press enter to close this windows now'
# SIG # Begin signature block
# MIIFjAYJKoZIhvcNAQcCoIIFfTCCBXkCAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUJa9ARX3+uQNS2MUvK4JbP5tF
# ovGgggMrMIIDJzCCAhOgAwIBAgIQUMOE90IF87JOyin4fsXBAzAJBgUrDgMCHQUA
# MBYxFDASBgNVBAMTC0NoYW50aXNuYWtlMB4XDTE2MDYxNjE1NDU0OFoXDTM5MTIz
# MTIzNTk1OVowLzEtMCsGA1UEAxMkQ2hhbnRpc25ha2UgKGdpdGh1Yi5jb20vY2hh
# bnRpc25ha2UpMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy7Ncif6x
# lH1QGb1b4EaZ0nGAItzoUl9YHgLBLIEe6Fvej0UFLptw9Z7NYlD9grfjqd5/D3Ju
# VN1MGdVrYNPmkf+UZEeFdQ7AnnktAdsr1ju7FDJrlmPg7F2WheCxJk0ge3R42ZeR
# deAo24WvBurIwn7FEDdKhyN2XIYAWFMpWEteTUQbs+6z2QFdKTWnvEOTvNAMrggB
# GbhpkQUCNVTV4Gu/Dfs0c+lRkR0gK8SmJhBp0uPP4Q6wVgddBNjyjSew6cePuU6b
# 80lDxV4MKGbaLeZZTOdijz0ZfOd2ET0tUZUPaaIW8yeq11rLFZfRmpEqFT8G/tvu
# sCVAmLgSBqlYfwIDAQABo2AwXjATBgNVHSUEDDAKBggrBgEFBQcDAzBHBgNVHQEE
# QDA+gBCXlTD6U/slFtHgpRwmm3y2oRgwFjEUMBIGA1UEAxMLQ2hhbnRpc25ha2WC
# ENjP+I016UCFTEgjw94CcnwwCQYFKw4DAh0FAAOCAQEAbSYjFr+ACprHJ+4AVcB0
# hvfl5sDDTCo1i0PRDFwwKvR7QfeGi6uKLpGc2EAkIfAGmdsbGlcqPrw5ypRuLk0r
# hXxh3hlfnUHj04K1EVxjpBysXsm7h2TWwfLIjwqH/aNoHM8siWcvDZjjwQ28XH9n
# SUVKuqLN5rYnk3IMp6jbakkRVVw4iyg/lR9PMf6Ss73f15XL/2nYDtdnkc1o3soO
# ywx+zyoct2belwR+Rj5c8zwsKXJhZ2qzY0YOO/KHzJM310PYtQ/4VGCgvBIjt2+E
# z+XnQ3TsNO/M1Tb/Y/UxBRaVvZc4Yb+75sP1BWThYmKq+gjByIWxEkd6+7pHGX5T
# 9TGCAcswggHHAgEBMCowFjEUMBIGA1UEAxMLQ2hhbnRpc25ha2UCEFDDhPdCBfOy
# Tsop+H7FwQMwCQYFKw4DAhoFAKB4MBgGCisGAQQBgjcCAQwxCjAIoAKAAKECgAAw
# GQYJKoZIhvcNAQkDMQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEOMAwGCisG
# AQQBgjcCARUwIwYJKoZIhvcNAQkEMRYEFLYCRcJBiTJq7bbzCcq72941cnnIMA0G
# CSqGSIb3DQEBAQUABIIBAI5pVcxUibeblhPZ2z00Q2hZURvyEjxK/GIioa8AcovI
# qlkkuz35CE0ApuSH+olTQUDob2oBXZcfLzSJkEXzuoWkyhxVgQAf0jcmrNAFTH7o
# RO88mZjMbuGmaxxxYtuICOJpjbJYQTVDAWIZNuM7TJ2v1ewMTVrzUXJbHYwKuhE/
# y1SHj9iFd4nBPnDYsiZ6xzY0TpAiKA+vYFg0l5ns6gC+TKLdV6i1lWKw91KZxeRw
# mVdI2YycEu9oklKhS2vqogtXNUBkyLzApgwhVnBGgwF1ZrY/5hrI/9KR+3+eSpzD
# DcVXcBKsjdaXJAVzFqGXkf4dLAgcg22m3hrbfsY80gg=
# SIG # End signature block
