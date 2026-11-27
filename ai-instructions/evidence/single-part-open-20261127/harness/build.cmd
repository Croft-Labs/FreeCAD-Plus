@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if errorlevel 1 exit /b %errorlevel%
set "TEMP=C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\temp"
set "TMP=%TEMP%"
set "PYTHONDONTWRITEBYTECODE=1"
set "PATH=C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\dependencies\LibPack-1.1.0-v3.1.1.3-Release\bin;C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\tools\ninja;%PATH%"
"C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\tools\cmake-3.31.6-windows-x86_64\bin\cmake.exe" --build "C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\build" --parallel 6 --target FreeCADPlusScripts
exit /b %errorlevel%

