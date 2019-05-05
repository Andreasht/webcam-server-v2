#!/bin/sh
fswebcam --no-banner -r 1920x1080 image.png		# tag billede med fswebcam kommando

b64=$(base64 image.png)					# kod billedet til base64
echo $b64 >> b64.txt					# skriv base64 data til tekstfil
