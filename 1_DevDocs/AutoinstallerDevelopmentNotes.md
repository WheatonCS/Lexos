# Auto-installer Development Notes

## Transferred from Issue #427
Theoretically changing the version number in \install\windows\config.ps1 will work.

If it does not, here is how the scripts work.

###cmd's

All the cmd scripts are helper scripts that actually calls powershell scripts (ps1).

  * `install.cmd` goes to the temp dir of the user(`~\AppData\Local\temp`) and then downloads the `install.ps1` and then triggers `install.ps1`.
  * `run.cmd`: This is created by `install.ps1` to run Lexos. That calls the local script: `run.ps1`, which should be located at `$lexosExecutableLocation = "$lexosLocation\install\windows\"`. See [config.ps1 L5](https://github.com/WheatonCS/Lexos/blob/master/install/windows/config.ps1#L5) for more detail.
  * `update.cmd`: This directly downloads the string of `update.cmd` and then eval (or `invoke-expression` in powershell) the string.

Therefore the local version of `install.cmd`, `update.ps1`, `install.ps1` actually never runs.

### ps1's

This is the tricky part, but because of the awesomeness of powershell, it is actually very easy to read.

#### install.ps1
This file first goes to https://repo.continuum.io/archive/, and then goes through the table to find the latest version of Anaconda, checks the hash, and then installs it.

**Note: Because the security issue of MD5, Continuum recently changed all their verification methods from MD5 to SHA256. This archive page still uses the outdated MD5. When they change it, we will need to change our script as well.**

This script then goes to the Lexos release page and downloads the release with the [version number](https://github.com/WheatonCS/Lexos/blob/master/install/windows/config.ps1#L2) you specified.

It then creates the shortcut, installs modules, and other stuff.

#### run.ps1
This script opens a cmd running python (but does not display the output, the output is redirected to null). It then continuously tries to connect to `http://localhost:5000`. When it succeeds, the default browser opens.

#### update.ps1
This script will first check whether the version you specify in `config.ps1` is already installed. If not, it removes all the other versions of Lexos (basically `C:\Lexos-*`) and then installs the new version of Lexos.


### other cool stuff.
The `lexos_installer.exe` is made with http://bat2exe.net/ and `install.cmd`.
The `lexos_installer.exe` (also `install.cmd` and `install.ps1`) accepts two switches: `-noAnaconda` and `-noConfirm`(alias: `-y`).

`-noAnaconda` will turn off Anaconda installation and download for testing.

`-y` will disable all the confirmations and prompts.

If you want to sign the `exe` or `ps1` file (you should, if you create a new exe or ps1) use the method here: https://github.com/GeeLaw/psguy.me/tree/master/profile#sign-scripts and the code can be found here: https://github.com/GeeLaw/psguy.me/blob/master/profile/profile.ps1#L32.
