import cv2
import numpy as np


def denoising_one(image_path):

    img = cv2.imread(image_path)

    # 마스크 만들기
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Refine mask with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    sky_mask = cv2.bitwise_not(mask)

    sky = cv2.bitwise_and(img, img, mask=sky_mask)
    sky_denoised = cv2.bilateralFilter(sky, d=7, sigmaColor=50, sigmaSpace=50)
    sky_denoised = cv2.fastNlMeansDenoisingColored(
        sky_denoised, None, h=10, hColor=10, searchWindowSize=21
    )

    buildings = cv2.bitwise_and(img, img, mask=mask)

    result = cv2.add(sky_denoised, buildings)
    result_float = result.astype(np.float32) / 255.0

    result_float = result_float * 0.75
    result_float = np.clip(result_float, 0, 1)
    result = (result_float * 255).astype(np.uint8)
    alpha = 1.1  # Contrast control (1.0-3.0)
    beta = -10  # Brightness control (-100 to 100)
    result = cv2.convertScaleAbs(result, alpha=alpha, beta=beta)

    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Denoised Result", result)

    # cv2.imwrite("result_01.png", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result


url = "denoising/img/01.png"
denoised_image = denoising_one(url)
