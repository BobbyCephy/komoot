chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set folder=%USERPROFILE%\OneDrive\komoot
set gpx=%folder%\gpx
if not exist %gpx% mkdir %gpx%
cd /d %gpx%
if exist credentials.json del credentials.json
komootgpx -s -r -m Robert.Kampf@gmx.de -p Golden.44x2 -a -o %gpx%
python "%~dp0gpx_to_kml.py" %gpx%\*.gpx
if exist credentials.json del credentials.json
start "" "%folder%"