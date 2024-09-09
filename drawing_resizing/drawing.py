"""_instruction_
- Left-click: Draw circle
- Ctrl+left-click: Start/continue polygon
- Ctrl+shift+left-click: Continue polygon
- Ctrl+left-click (no Shift): End polygon
- Press Enter to save image
- Press Esc to exit
"""

import sys
import cv2
import numpy as np
import random

LINE_WIDTH = 2
WIDTH, HEIGHT = 512, 512


def draw():
    img = np.zeros((WIDTH, HEIGHT, 3), np.uint8) + 255
    poly_points = []
    is_drawing = False

    def mouse_callback(event, x, y, flags, param):
        nonlocal is_drawing, poly_points

        if event == cv2.EVENT_LBUTTONDOWN:
            radius = random.randint(10, 50)
            line_width = random.randint(1, 2)
            cv2.circle(
                img,
                (x, y),
                radius,
                (
                    0,
                    0,
                    0,
                ),
                line_width,
            )
        elif event == cv2.EVENT_LBUTTONDOWN:
            # is_drawing: False ? 처음 드로잉 시작
            # -> is_drawing: True로 바꾸고 찍은 포인트를 points에 append
            if not is_drawing:
                is_drawing = True
                poly_points.append((x, y))
            else:
                cv2.line(img, poly_points[-1], (x, y), (255, 0, 255), line_width)
                poly_points.append((x, y))
            # is_drawing: True ?
            # points에 포인트 append
            # 이전 포인트와 현재 포인트로 폴리선 그리기

    cv2.namedWindow("Drawing")
    cv2.setMouseCallback("Drawing", mouse_callback)

    while True:
        display_img = img.copy()
        cv2.putText(
            display_img,
            "Press Enter to save image, Press Esc to exit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
        )
        cv2.imshow("Drawing", display_img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 13:
            cv2.imwrite("my_drawing.png", display_img)
            print("Image saved.")
            break
    cv2.destroyAllWindows()


draw()
