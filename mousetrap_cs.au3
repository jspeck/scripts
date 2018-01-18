;
;  AutoIt Script
;
;  Traps mouse cursor in your cs window
;  Press F8 to close
;

#include <Misc.au3>
#include <TrayConstants.au3>
#include <MsgBoxConstants.au3>

TrayTip("", "Mouse Trap Opened", 5, $TIP_NOSOUND )

While True
   If _isPressed(77) Then	; F8
	  ExitLoop
   EndIf

   If WinActive("[TITLE:Counter-Strike]") Then
	  _MouseTrap(0, 0, 1920, 1080)
   EndIf

WEnd

TrayTip("", "Mouse Trap Closed", 5, $TIP_NOSOUND )
Sleep(5000)

