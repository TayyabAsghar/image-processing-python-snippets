import imghdr
import imagehash
import numpy as np
from pathlib import Path
from PIL import Image, UnidentifiedImageError

# Custom Library
from colored_text import Text

""" 
Duplicate Image Finder (DIF) by HASH: function that searches a given directory for images and finds duplicate/similar images among them.
Outputs the number of found duplicate/similar image pairs.
"""


class HashFinder:
    def __init__(self, directory, hash_size=8):
        """
        directory (str).........folder to search for duplicate images
        hash_size (int).........sizeof our hash
        """
        assert (
            Path(directory).exists() == True
        ), f'{Text.ERROR} "{directory}" does\'t exist.'
        # Taking only files names
        self.__image_files = [
            x for x in Path(directory).glob("*.*") if x.is_file() and imghdr.what(x)
        ]
        self.__hash_size = hash_size

    def duplicate(self, remove=False):
        """
        remove (bool)...........True = remove the duplicature files
                                False = only print the duplicate files
        """

        hashes = {}
        duplicates = []

        print(f"\n{Text.PROCESSING} Finding Duplicates !!!\n")

        for image in self.__image_files:
            try:
                with Image.open(image) as img:
                    temp_hash = imagehash.average_hash(img, self.__hash_size)

                    if temp_hash in hashes:
                        # print(
                        #     "{} Duplicate {} \nfound for Image {}!\n".format(
                        #         Text.EXC, image, hashes[temp_hash]
                        #     )
                        # )
                        duplicates.append(image)
                    else:
                        hashes[temp_hash] = image
            except UnidentifiedImageError:
                self.__image_files.remove(image)
                print(
                    f'{Text.ERROR} "{image}" can\'t open by PIL so Removed from list.'
                )

        if len(duplicates) != 0:
            print(
                f"{Text.DONE} Found {len(duplicates)} duplicate image pairs in {len(self.__image_files)} total images."
            )

            if remove:
                print(f"{Text.INFO} Start removing the Duplicate Images !!!\n")
                for duplicate in duplicates:
                    Path(duplicate).unlink()
                    print(f"{Text.DONE} {duplicate} Deleted Successfully !!!")
            else:
                print(f"{Text.INFO} List of Duplicate Images :")

                for duplicate in duplicates:
                    print(f"{Text.EXC} {duplicate}")

        else:
            print(f"{Text.INFO} No Duplicates Found :(")

        # Converting Posix Paths to strings
        return set(map(str, duplicates))

    def similar(self, image, similarity=80):
        """
        image (str).............image path for similar image
        similarity (int)........to what percent images should be similar
        """

        assert Path(image).exists() == True, f'{Text.ERROR} "{image}" does\'t exist.'

        threshold = 1 - (similarity / 100)
        diff_limit = int(threshold * (self.__hash_size ** 2))
        similar = []

        with Image.open(image) as img:
            hash1 = imagehash.average_hash(img, self.__hash_size).hash

        print(f"\n{Text.PROCESSING} Finding Similar Images to {image} !!!\n")

        for img in self.__image_files:
            with Image.open(img) as img:
                hash2 = imagehash.average_hash(img, self.__hash_size).hash

                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    similar.append(img)
                    print(
                        f"{Text.TICK} {img} image found {similarity}% similar to {image}"
                    )

        # Converting Posix Paths to strings
        return set(map(str, similar))
