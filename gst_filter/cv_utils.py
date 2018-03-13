import cv2


def grayscale(img):   
    """
        Convert colored image to Grayscale

        :param img: [height, width, channels >= 3]
        :type img: np.ndarray

        :rtype: np.ndarray
    """
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gaussian_blur(img, kernel_size=3, sigma=(1, 1)):  
    """
        Blur image

        :param img: [height, width, channels >= 3]
        :type img: np.ndarray

        :param kernel_size:
        :type kernel_size: int

        :param sigma: [height, width, channels >= 3]
        :type sigma: tuple -> (int, int)

        :rtype: np.ndarray
    """  
    sigmaX, sigmaY = sigma
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigmaX=sigmaX, sigmaY=sigmaY)