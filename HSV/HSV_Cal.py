import cv2 as cv
import numpy as np


class HSV_Cal:
    def __init__(self):
        # Initialize HSV min/max values
        self.hMin = self.sMin = self.vMin = self.hMax = self.sMax = self.vMax = 0

    def __createTrackbarWindow__(self, windowName):
        def nothing2(x):
            print(f"x ======= {x}")
            # print(f"value ======= {y}")
            pass

        def nothing(x):
            pass

        # Create a window
        cv.namedWindow(windowName)

        # Create trackbars for color change
        # Hue is from 0-179 for Opencv
        cv.createTrackbar("HMin", windowName, 0, 179, nothing2)
        cv.createTrackbar("SMin", windowName, 0, 255, nothing)
        cv.createTrackbar("VMin", windowName, 0, 255, nothing)
        cv.createTrackbar("HMax", windowName, 0, 179, nothing)
        cv.createTrackbar("SMax", windowName, 0, 255, nothing)
        cv.createTrackbar("VMax", windowName, 0, 255, nothing)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos("HMax", windowName, 179)
        cv.setTrackbarPos("SMax", windowName, 255)
        cv.setTrackbarPos("VMax", windowName, 255)

    def __getTrackbarsPos__(self, windowName):
        # Get current positions of all trackbars
        self.hMin = cv.getTrackbarPos("HMin", windowName)
        self.sMin = cv.getTrackbarPos("SMin", windowName)
        self.vMin = cv.getTrackbarPos("VMin", windowName)
        self.hMax = cv.getTrackbarPos("HMax", windowName)
        self.sMax = cv.getTrackbarPos("SMax", windowName)
        self.vMax = cv.getTrackbarPos("VMax", windowName)

    def Image(self, filename, flags=cv.IMREAD_COLOR, printVal=True):

        # Load image
        image = cv.imread(filename, flags)

        self.__createTrackbarWindow__("image")

        phMin = psMin = pvMin = phMax = psMax = pvMax = 0

        # Remove the unbound error
        lower = upper = 0

        while 1:
            self.__getTrackbarsPos__("image")

            # Set minimum and maximum HSV values to display
            lower = np.array([self.hMin, self.sMin, self.vMin])
            upper = np.array([self.hMax, self.sMax, self.vMax])

            # Convert to HSV format and color threshold
            hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lower, upper)
            result = cv.bitwise_and(image, image, mask=mask)

            if (
                (phMin != self.hMin)
                | (psMin != self.sMin)
                | (pvMin != self.vMin)
                | (phMax != self.hMax)
                | (psMax != self.sMax)
                | (pvMax != self.vMax)
            ):
                if printVal:
                    print(
                        f"(hMin = {self.hMin}, hMax = {self.hMax}) (sMin = {self.sMin}, sMax = {self.sMax}), (vMin = {self.vMin}, vMax = {self.vMax})"
                    )

                phMin = self.hMin
                psMin = self.sMin
                pvMin = self.vMin
                phMax = self.hMax
                psMax = self.sMax
                pvMax = self.vMax

            # Display result image
            cv.imshow("image", result)

            if cv.waitKey(1) == 27:
                break

        cv.destroyAllWindows()

        return lower, upper

    def VideoCapture(self, video, printVal=True):

        cap = cv.VideoCapture(video)

        self.__createTrackbarWindow__("video")

        phMin = psMin = pvMin = phMax = psMax = pvMax = 0

        # Remove the unbound error
        lower = upper = 0

        while 1:
            ret, frame = cap.read()
            self.__getTrackbarsPos__("video")
            # Set minimum and maximum HSV values to display
            lower = np.array([self.hMin, self.sMin, self.vMin])
            upper = np.array([self.hMax, self.sMax, self.vMax])

            # Convert to HSV format and color threshold
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lower, upper)
            result = cv.bitwise_and(frame, frame, mask=mask)

            # Print if there is a change in HSV value
            if (
                (phMin != self.hMin)
                | (psMin != self.sMin)
                | (pvMin != self.vMin)
                | (phMax != self.hMax)
                | (psMax != self.sMax)
                | (pvMax != self.vMax)
            ):
                if printVal:
                    print(
                        f"(hMin = {self.hMin}, hMax = {self.hMax}) (sMin = {self.sMin}, sMax = {self.sMax}), (vMin = {self.vMin}, vMax = {self.vMax})"
                    )

                phMin = self.hMin
                psMin = self.sMin
                pvMin = self.vMin
                phMax = self.hMax
                psMax = self.sMax
                pvMax = self.vMax

            # Display result frames
            cv.imshow("video", result)

            if cv.waitKey(1) == 27:
                break

        cap.release()
        cv.destroyAllWindows()

        return lower, upper
