# 0906 De-noising Project
import cv2
import numpy as np

org1 = "denoising/img/mission_image01.png"
url1 = "denoising/img/01.png"

img = cv2.imread(url1)

bilateral = cv2.bilateralFilter(src=img, d=7, sigmaColor=50, sigmaSpace=30)
sharpened = cv2.addWeighted(img, 1.5, bilateral, -0.5, 0)

# 칼라노이즈 제거에 효과적
nl_means = cv2.fastNlMeansDenoisingColored(sharpened, None, h=10, hColor=10)

# 블랜딩
blending = cv2.addWeighted(nl_means, 0.7, sharpened, 0.3, 0)

# 외곽이 뭉개지지 않는 선에서 남아있는 하늘의 노이즈를 살짝 제거한다.
result = cv2.GaussianBlur(nl_means, (3, 3), 0.3)

img_float = result.astype(np.float32) / 255.0
img_float = img_float * 0.7
img_adjusted = (img_float * 255).astype(np.uint8)
alpha = 1.1  # Contrast control (1.0-3.0)
beta = -10  # Brightness control (-100 to 100)
img_final = cv2.convertScaleAbs(img_adjusted, alpha=alpha, beta=beta)


# Display results
cv2.imshow("Original", img)
cv2.imshow("Result", img_final)

# cv2.imwrite("result_nomask_01.png", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
