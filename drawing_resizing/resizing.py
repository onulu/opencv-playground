import cv2


def resizing(img, kernel=(3, 3), fx=0.25, fy=0.25):
    src = cv2.imread(img)
    blurred = cv2.blur(src, kernel)

    inter_area = cv2.resize(blurred, None, fx=fx, fy=fy, interpolation=cv2.INTER_AREA)
    inter_linear = cv2.resize(
        blurred, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR
    )

    cv2.imshow("org", src)
    cv2.imshow("area", inter_area)
    cv2.imshow("linear", inter_linear)

    # cv2.imwrite("drawing_resizing/inter_area.png", inter_area)
    # cv2.imwrite("drawing_resizing/inter_linear.png", inter_linear)
    cv2.waitKey()
    cv2.destroyAllWindows()
    pass


resizing("drawing_resizing/my_drawing.png")
