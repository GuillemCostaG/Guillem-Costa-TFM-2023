import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import cv2


image = cv2.imread('Imatges/platja1.PNG')
image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
image_gray = image_gray.astype(np.float64)
w = signal.windows.gaussian(5, 1.0)
image_new = signal.sepfir2d(image_gray, w, w)

plt.figure()
plt.imshow(image_gray, cmap='gray')
plt.title('Original image')
plt.show()

plt.figure()
plt.imshow(image_new)
plt.gray()
plt.title('Filtered image')
plt.show()