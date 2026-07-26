set folder=%USERPROFILE%\OneDrive\gpx\komoot
if not exist %folder% mkdir %folder%
cd %folder%
del credentials.json
komootgpx -s -r -m Robert.Kampf@gmx.de -p Golden.44x2 -a -o %folder%
del credentials.json
start "" "%folder%"