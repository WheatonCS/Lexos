$ErrorActionPreference = 'Inquire'
Import-Module BitsTransfer

# go to the temp dir
$location = Get-Location
Set-Location $HOME/AppData/Local/Temp/

# get current location
$curLocation = Get-Location

# installing anaconda
Write-Host 'fetching anaconda archieve' -ForegroundColor Green
$anacondaUrl = 'https://repo.continuum.io/archive/'
$anacondaWebPage = Invoke-WebRequest $anacondaUrl

Write-Host ' '
Write-Host 'analysing the HTML' -ForegroundColor Green
$anacondaHTML = $anacondaWebPage.parsedHTML
$archieves = $anacondaHTML.body.getElementsByTagName('TR')

foreach ($archieve in $archieves) {
    
    # extract information
    $dataItems = $archieve.children
    $binItem = $dataItems[0]
    $SizeItem = $dataItems[1]
    $timeItem = $dataItems[2]
    $hashItem = $dataItems[3]
    
    # see if the process is 64 bit
    if([Environment]::Is64BitProcess) {
        $nameRegex = 'Anaconda2-.*-Windows-x86_64.exe'
    }
    else {
        $nameRegex = 'Anaconda2-.*-Windows-x86.exe'
    }
    
    if($binItem.innerText -match $nameRegex){  # this is the latest version    
        # output infomation
        $name = $binItem.innerText
        $size = $SizeItem.innerText
        $time = $timeItem.innerText
        $hash = $hashItem.innerText
        Write-Host 'found the latest release of anaconda2'
        Write-Host "name of the file is: $name"
        Write-Host "the size of the file is: $size"
        Write-Host "the last modified time is: $time"
        Write-Host "the hase(MD5) is: $hash"
        
        # download the installer
        Write-Host ' '
        Write-Host 'downloading the anaconda2 installer' -ForegroundColor Green
        Write-Host 'this could takes a while' -ForegroundColor Green
        $fileUrl = "https://repo.continuum.io/archive/$name"
        Start-BitsTransfer $fileUrl ./anaconda_installer.exe -DisplayName 'Downloading the Latest Version of Anaconda2...'
        
        # check MD5
        Write-Host ' '
        Write-Host 'Checking MD5 value' -ForegroundColor Green
        $localHash = Get-FileHash ./anaconda_installer.exe -Algorithm MD5 
        if($localHash.Hash.ToUpper() = $hash.ToUpper()){
            Write-Host 'MD5 hash is good'
        }
        else {
            Write-Host 'The MD5 value is not the same, if you continue you maybe exposed to malware or virus' -ForegroundColor Red
            Write-Host 'Please check you network setting and try again. There maybe a proxy setted up' -ForegroundColor Red
            Read-Host 'Press Enter to continue, press Ctrl-C to stop'
        }
        
        # run the installer
        Write-Host ''
        Write-Host 'installing anaconda2, this should take a long time' -ForegroundColor Green
        Write-Host 'sorry we cannot display the process of installing' -ForegroundColor Green
        Write-Host 'Please sit back and relax' -ForegroundColor Green
        ./anaconda_installer.exe /AddToPath=0  /InstallationType=JustMe /S /D=$HOME\Anaconda2\ | Out-Null
        break
    }
}

# installing lexos
if(Test-Path 'C:\Lexos-master'){
    Write-Host ' '
    Write-Host 'you already have lexos installed'
    Write-Host 'run update.exe to update'
}
else {
    Write-Host ' '
    Write-Host 'downloading lexos' -ForegroundColor Green
    Write-Host 'This could take a while...' -ForegroundColor Green
    Write-Host 'Sorry we cannot display the status of the download, because it slows down the download' -ForegroundColor Green
    Write-Host 'Please sit back and relax' -ForegroundColor Green
    $lexosUrl = 'https://github.com/WheatonCS/Lexos/archive/master.zip'
    (new-object net.webclient).DownloadFile($lexosUrl, "$curLocation/master.zip")
    Write-Host ' '
    Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
    Expand-Archive -Path "$curLocation\master.zip" -DestinationPath "C:\"
}


# installing requirements
Write-Host ' '
Write-Host 'installing other requirements (python modules)' -ForegroundColor Green
Invoke-Expression "$HOME\Anaconda2\Scripts\pip.exe install -r C:\Lexos-master\requirement.txt"

# creating desktop icon
Write-Host ' '
Write-Host 'creating desktop icon for you ^_^' -ForegroundColor Green
$desktop = [System.Environment]::GetFolderPath('Desktop')
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
$Shortcut.IconLocation = "C:\Lexos-master\install\assets\Lexos.ico"
$shortcut.Save()

# go back 
Set-Location $location

# final message
Write-Host ' '
Write-Host 'lexos developer edition is successfully installed in "C:\Lexos-master"' -ForegroundColor Green
Write-Host 'if you want to uninstall lexos just remove that folder' -ForegroundColor Green
Write-Host 'thank you for using lexos.' -ForegroundColor Green
Read-Host 'press Enter to quit'


# SIG # Begin signature block
# MIIFjAYJKoZIhvcNAQcCoIIFfTCCBXkCAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUAVU6OLeCYT8ag+e1EJqol22L
# YUegggMrMIIDJzCCAhOgAwIBAgIQUMOE90IF87JOyin4fsXBAzAJBgUrDgMCHQUA
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
# AQQBgjcCARUwIwYJKoZIhvcNAQkEMRYEFGcvH4b0YiNkU4MA+f6PzRrkttljMA0G
# CSqGSIb3DQEBAQUABIIBAIzfcuFElDDrf0DKvMitMK8CAcC2+U/QhO3SrH0qCevb
# DAaZTvzj1uaDhyPtpFx3h2uLeQS5OxI6vQXBYaMlz2/Z5xTj3rdKkt6hpbPjuGFx
# 7MOK0kxt+JN0Bc3Dak4hJEHiwKSynTE38Kp77K0Xufav4KtqDPlNf2RWtG+vO9F5
# T48Ievtb/SZyN2ycujyueIDG+9kYGpa9Kqbcf3XO8E/0pIUJDZ92Ug3P5uk7SDIn
# jMpC9uMNB4TEc+27Q1QjHoMunbVCe9SVLsZLjlNfwzemzlcx7WL8h87GuR/1XsrH
# 0B+Awe5w5qGkMFbwFqJZHTGeDMx1R7BQyvzVy/l0IzY=
# SIG # End signature block
