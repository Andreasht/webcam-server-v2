#!/bin/sh
fswebcam --no-banner -r 1920x1080 image.png

b64=$(base64 image.png)
echo $b64 >> b64.txt
