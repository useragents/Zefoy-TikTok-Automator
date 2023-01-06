# Changes Log
Open-Source Contribution: itzCozi

## Minor changes
- Pip must be installed if install.bat is ran
- Both batch files were updated then combined to create Lazy-Installer
- Added documentation and cleaned up code
- Removed overly long title changer
- Changed some feedback given to the user

## Compatiblity patch
The function you use for changing the title of the window only works on windows and uses a faluty package to fix this I added a function that dectects linux kernal and the title is not changed.

## ctypes.windll error
In order to change the title of the window your function uses the package ctypes and I think after a recent update a command that your script uses got deprecated. Therefore i also had troubles with it but it should be fixed now.

## MIT License
Almost all of my contributions are MIT or GNU but you don't have a license if you had a MIT license developers would come and contribute to your projects and make a little developer tribe but the MIT license also means a group as a whole worked on it, never only one face, Always free and open meaning anyone can submit a pull request.

### Multipule miscellaneous changes not recored.