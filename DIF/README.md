# DIF

This snippet is used find the Duplicate / Similar Images in a Directory. Their are 2 ways to find duplicate images.

- By [Hash Method][hash]
- By [Mean Square Error Method][mse]

## ⚡️ Usage

```py
# First copy the folder in the project.

# For Hash Method
from DIF import HashFinder

# For Mean Square Error Method
from DIF import MeanFinder

# For all the Duplicate images in a Directory.
dup_imgs = HashFinder(directory).duplicate()

# For finding similar image of given image in a Directory.
sim_imgs = HashFinder(directory).similar(image, similarity=70)

# For all the Duplicate images in a Directory.
dup_imgs = MeanFinder(directory)
```

```py
HashFinder(directory, hash_size=8).duplicate(remove=False)

'''
directory - Directory to search for duplicate images
hash_size - Size of our hash. By default it is 8x8.
remove    - True = remove the duplicature files
            False = only print the duplicate files
'''

HashFinder(directory, hash_size=8).similar(image, similarity=70)

'''
directory  - Directory to search for duplicate images
hash_size  - Size of our hash. By default it is 8x8.
remove     - True = remove the duplicature files
             False = only print the duplicate files
image      - Image path for similar image.
similarity - To what percent images should be similar.
'''
```

## 📦 Requirements

- Pillow
- Pathlib
- Imghdr
- Numpy
- colorama
- OpenCV
- Matplotlib
- ImageHash

<!-- Links -->

[hash]: https://medium.com/@somilshah112/how-to-find-duplicate-or-similar-images-quickly-with-python-2d636af9452f
[mse]: https://towardsdatascience.com/finding-duplicate-images-with-python-71c04ec8051
