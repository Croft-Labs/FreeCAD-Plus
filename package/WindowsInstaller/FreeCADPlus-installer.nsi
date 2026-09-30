; SPDX-License-Identifier: LGPL-2.1-or-later
; Build with NSIS 3: /DPAYLOAD=<staged install> /DOUTPUT=<installer.exe>
Unicode true
RequestExecutionLevel user
ManifestDPIAware true
SetCompressor /SOLID lzma
!include MUI2.nsh
!include x64.nsh
!ifndef PAYLOAD
  !error "Pass /DPAYLOAD=<staged install>"
!endif
!ifndef OUTPUT
  !error "Pass /DOUTPUT=<installer.exe>"
!endif
!define VERSION "0.0.4"
!define UNINSTALL_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\CroftLabs.FreeCADPlus.${VERSION}"
Name "FreeCAD Plus ${VERSION} Pre-Release"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\Programs\FreeCAD Plus ${VERSION}"
VIProductVersion "0.0.4.0"
VIAddVersionKey "ProductName" "FreeCAD Plus"
VIAddVersionKey "FileDescription" "FreeCAD Plus 0.0.4 Windows x64 installer"
VIAddVersionKey "FileVersion" "0.0.4.0"
VIAddVersionKey "LegalCopyright" "FreeCAD contributors; FreeCAD Plus changes by Croft-Labs"
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${PAYLOAD}\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
Function .onInit
  ${IfNot} ${RunningX64}
    MessageBox MB_ICONSTOP "FreeCAD Plus requires 64-bit Windows."
    Abort
  ${EndIf}
FunctionEnd
Section "FreeCAD Plus"
  SetShellVarContext current
  SetOutPath "$INSTDIR"
  File /r /x uninstall-files.nsh "${PAYLOAD}\*"
  WriteUninstaller "$INSTDIR\Uninstall-FreeCADPlus.exe"
  CreateDirectory "$SMPROGRAMS\FreeCAD Plus ${VERSION}"
  CreateShortcut "$SMPROGRAMS\FreeCAD Plus ${VERSION}\FreeCAD Plus.lnk" "$INSTDIR\FreeCADPlus.exe" "" "$INSTDIR\bin\FreeCAD.exe"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayName" "FreeCAD Plus ${VERSION} Pre-Release"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "Publisher" "Croft-Labs"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "UninstallString" '$\"$INSTDIR\Uninstall-FreeCADPlus.exe$\"'
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoRepair" 1
SectionEnd
Section "Uninstall"
  SetShellVarContext current
  ; Generated from the payload: removes only installed files, then empty dirs.
  !include "${PAYLOAD}\uninstall-files.nsh"
  Delete "$INSTDIR\Uninstall-FreeCADPlus.exe"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\FreeCAD Plus ${VERSION}\FreeCAD Plus.lnk"
  RMDir "$SMPROGRAMS\FreeCAD Plus ${VERSION}"
  DeleteRegKey HKCU "${UNINSTALL_KEY}"
  ; User preferences and documents are deliberately retained.
SectionEnd
