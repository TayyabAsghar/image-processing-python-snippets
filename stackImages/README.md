# Stack-Images

This function is used to stack multiple images in a single frame so we can easily see th results. It an also stack images of different chanel in the same frame.

## ⚡️ Usage

```py
# First copy the folder in the project.
from stackImages import stackImages
import cv2

# For Horizontal
hor_stack = stackImages(0.9,[img1,img2])

# For Horizontal
ver_stack = stackImages(0.9,[img1], [img2])

# for Both
stack = stackImages(0.9,[img1,img2],[img3,img4])

# For last one the number of images in both lists should be same. if you don't have same number of images you can produce one empty / black image.

# np.zeros_like(img3)

cv2.imshow(hor_stack)
cv2.imshow(ver_stack)
cv2.imshow(stack)
```

```py
stackImages(scale, imgArray)

'''
scale - Scale at which you wants to show images.
imgArray    - List of images.
'''
```

## 📦 Requirements

- OpenCV
- Numpy
