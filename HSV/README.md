# HSV

This class is used to calculate the HSV values of a colo in real time. It works on

- Images
- Videos
- Live Streams

For some understanding of HSV [click Here][hsv].

## ⚡️ Usage

```py
# First copy the folder in the project.

from HSV import HSV_Cal

# For Image.
hsv = HSV_Cal().Image(image_name)

# For Video or Camera.
hsv = HSV_Cal().VideoCapture(video_name)
```

```py
Image(filename, flags=cv.IMREAD_COLOR, printVal=True)

'''
filename - Name / Path of Image.
flags    - All cv2.imread() flags are applicable here.
printVal - Print HSV values on the terminal.
'''

VideoCapture(filename, printVal=True)

'''
filename - Name / Path of Video or Camera number.
printVal - Print HSV values on the terminal.
'''
```

## 📦 Requirements

- OpenCV
- Numpy

<!-- Links -->

[hsv]: https://upload.wikimedia.org/wikipedia/commons/f/f2/HSV_color_solid_cone.png
