import cv2
import numpy as np

url = "denoising/img/03.png"
img = cv2.imread(url)

# 필터적용
denoised = cv2.fastNlMeansDenoisingColored(img, None, 7, 7)

# 선명도 조절
kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpened = cv2.filter2D(denoised, -1, kernel)

result = cv2.addWeighted(denoised, 0.7, sharpened, 0.3, 0)

cv2.imshow("original", img)
cv2.imshow("sharpened", sharpened)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
