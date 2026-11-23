@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if errorlevel 1 exit /b %errorlevel%
"C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\tools\cmake-3.31.6-windows-x86_64\bin\cmake.exe" --build "C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\build" --target FreeCADApp FreeCADPlusScripts --parallel 6
exit /b %errorlevel%
