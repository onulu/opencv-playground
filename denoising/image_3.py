import cv2
import numpy as np

org = "denoising/img/mission_image05.png"
url = "denoising/img/05.png"

img = cv2.imread(url)

# 필터적용
denoised = cv2.fastNlMeansDenoisingColored(img, None, 7, 7)

# 밝기, 컨트라스트 조절
brightness = cv2.convertScaleAbs(denoised, alpha=1, beta=-25)

# 샤프닝 적용
kernel = np.array([[-0.25, -0.25, -0.25], [-0.25, 3.00, -0.25], [-0.25, -0.25, -0.25]])
result = cv2.filter2D(brightness, -1, kernel)

cv2.imshow("original", img)
cv2.imshow("Result", result)

# cv2.imwrite("result_03.png", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
