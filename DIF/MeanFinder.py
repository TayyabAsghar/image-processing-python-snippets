import cv2
import imghdr
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Custom Library
from colored_text import Text

""" 
Duplicate Image Finder (DIF) by Mean Square Error: function that searches a given directory for images and finds duplicate/similar images among them.
Outputs the number of found duplicate/similar image pairs with a list of the filenames having lower resolution.
"""


def MeanFinder(
    directory,
    show_imgs=False,
    similarity="high",
    compression=50,
    remove=False,
    rotate_check=True,
):
    """
    directory    - Directory to search for duplicate/similar images
    show_imgs    - True = shows the duplicate/similar images found in output
                   False = doesn't show found images
    similarity   - "high" = searches for duplicate images, more precise
                   "low" = finds similar images
    compression  - Recommended not to change default value
                   compression in px (height x width) of the images before being compared
                   the higher the compression i.e. the higher the pixel size, the more computational ressources and time required
    remove       - True = remove the duplicature files
                            False = only print the duplicate files
    rotate_check - True = rotate the file to check for comparision
                   False = doesn't rotate the image
    """
    assert (
        Path(directory).exists() == True
    ), f'{Text.ERROR} "{directory}" does\'t exist.'

    # list where the found duplicate/similar images are stored
    duplicates = []
    lower_res = []

    # search for similar images
    if similarity == "low":
        ref = 1000
    # search for 1:1 duplicate images
    else:
        ref = 200

    main_img = 0
    compared_img = 1
    nrows = ncols = compression
    srow_A = 0
    erow_A = nrows
    srow_B = erow_A
    erow_B = srow_B + nrows

    print(f"\n{Text.PROCESSING} Start Comparing !!!")

    imgs_matrix = __create_imgs_matrix(directory, compression)

    while erow_B <= imgs_matrix.shape[0]:
        while compared_img < (len(__image_files)):
            # select two images from imgs_matrix
            imgA = imgs_matrix[srow_A:erow_A, 0:ncols]  # rows  # columns
            imgB = imgs_matrix[srow_B:erow_B, 0:ncols]  # rows  # columns
            # compare the images
            rotations = 0
            while __image_files[main_img] not in duplicates:
                if rotations != 0 and rotate_check:
                    if rotations <= 3:
                        imgB = __rotate_img(imgB)
                        rotations += 1
                    else:
                        break

                err = __mse(imgA, imgB)
                if err < ref:
                    if show_imgs == True:
                        __show_img_figs(imgA, imgB, err)
                        __print_file_info(compared_img, main_img)
                    # Add to the list
                    duplicates.append(__image_files[main_img])
                    __check_img_quality(
                        __image_files[main_img], __image_files[compared_img], lower_res
                    )

            srow_B += nrows
            erow_B += nrows
            compared_img += 1

        srow_A += nrows
        erow_A += nrows
        srow_B = erow_A
        erow_B = srow_B + nrows
        main_img += 1
        compared_img = main_img + 1

    print(
        f"\n{Text.DONE} found {len(lower_res)} duplicate image pairs in total {len(__image_files)} images."
    )

    if remove:
        print(f"{Text.INFO} Start removing the Duplicate Images !!!\n")

        for image in lower_res:
            Path(image).unlink()
            print(f"{Text.DONE} {image} Deleted Successfully !!!")
    else:
        print(f"{Text.INFO} The following files have lower resolution:")

        for image in lower_res:
            print(f"{Text.EXC} {image}")

    # Converting Posix Paths to strings
    return set(map(str, lower_res))


# Function that searches the folder for image files, converts them to a matrix
def __create_imgs_matrix(directory, compression):
    global __image_files
    __image_files = []

    # create list of all files in directory
    folder_files = [
        x for x in Path(directory).glob("*.*") if x.is_file() and imghdr.what(x)
    ]

    # create images matrix
    counter = 0
    for filename in folder_files:
        img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if type(img) == np.ndarray:
            img = img[..., 0:3]
            img = cv2.resize(
                img, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC
            )
            if counter == 0:
                imgs_matrix = img
                __image_files.append(filename)
                counter += 1
            else:
                try:
                    imgs_matrix = np.concatenate((imgs_matrix, img))
                except ValueError:
                    folder_files.remove(filename)
                    print(ValueError)
                __image_files.append(filename)
    return imgs_matrix


# Function that calculates the mean squared error (mse) between two image matrices
def __mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


# Function that plots two compared image files and their mse
def __show_img_figs(imageA, imageB, err):
    fig = plt.figure()
    plt.suptitle("MSE: %.2f" % (err))

    # plot first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    # plot second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()


# Function for rotating an image matrix by a 90 degree angle
def __rotate_img(image):
    return np.rot90(image, k=1, axes=(0, 1))


# Function for printing filename info of plotted image files
def __print_file_info(compared_img, main_img):
    print(
        f"{Text.INFO} Duplicate file: {__image_files[main_img]} and {__image_files[compared_img]}."
    )


# Function for checking the quality of compared images, appends the lower quality image to the list
def __check_img_quality(imageA, imageB, list):
    size_imgA = imageA.stat().st_size
    size_imgB = imageB.stat().st_size

    if size_imgA > size_imgB:
        list.append(imageB)
    else:
        list.append(imageA)
