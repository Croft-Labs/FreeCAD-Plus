; SPDX-License-Identifier: LGPL-2.1-or-later
Unicode true
RequestExecutionLevel user
SilentInstall silent
!include FileFunc.nsh
!ifndef OUTPUT
  !error "Pass /DOUTPUT=<launcher path>"
!endif
Name "FreeCAD Plus"
OutFile "${OUTPUT}"
Section
  ; Keep fork preferences, macros and caches separate from upstream FreeCAD.
  System::Call 'Kernel32::SetEnvironmentVariableW(w "FREECAD_USER_HOME", w "$APPDATA\FreeCADPlus")'
  System::Call 'Kernel32::SetEnvironmentVariableW(w "FREECAD_USER_DATA", w "$APPDATA\FreeCADPlus")'
  System::Call 'Kernel32::SetEnvironmentVariableW(w "FREECAD_USER_TEMP", w "$LOCALAPPDATA\FreeCADPlus\Temp")'
  CreateDirectory "$APPDATA\FreeCADPlus"
  CreateDirectory "$LOCALAPPDATA\FreeCADPlus\Temp"
  ${GetParameters} $0
  SetOutPath "$EXEDIR"
  Exec '"$EXEDIR\bin\FreeCAD.exe" $0'
SectionEnd
