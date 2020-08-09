SET CANDLE="C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe"
SET LIGHT="C:\Program Files (x86)\WiX Toolset v3.11\bin\light.exe"

Del Setup\*.wixpdb
Del Setup\*.wixobj
Del Setup\*.msi

%CANDLE% ".\TinyPID.wxs" -out .\Setup\
IF %ERRORLEVEL% NEQ 0 goto :ERROR
%LIGHT% -out ".\Setup\TinyPID-%1.msi" ".\Setup\TinyPID.wixobj" -ext WixUIExtension -ext WixUtilExtension
IF %ERRORLEVEL% NEQ 0 goto :ERROR

:EOF
ECHO process completed 
REM exit

:ERROR
REM exit 1