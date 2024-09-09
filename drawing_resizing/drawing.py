import cv2
import random
import numpy as np

WIDTH, HEIGHT = 512, 512


def draw_multiline_text(img, text, pos):
    for i, line in enumerate(text.split("\n")):
        cv2.putText(
            img,
            line,
            (pos[0], pos[1] + i * 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
        )


def draw():
    img = np.zeros((HEIGHT, WIDTH, 3), np.uint8) + 255
    poly_points = []
    is_drawing = False
    mode = "Circle"

    def mouse_callback(event, x, y, flags, _):
        nonlocal is_drawing, poly_points, img

        if event == cv2.EVENT_LBUTTONDOWN:
            if mode == "Circle":
                cv2.circle(
                    img, (x, y), random.randint(10, 50), (0, 0, 0), random.randint(1, 2)
                )
            elif mode == "Polygon":
                if not is_drawing:
                    is_drawing = True
                    poly_points = [(x, y)]
                else:
                    poly_points.append((x, y))
                    if not flags & cv2.EVENT_FLAG_SHIFTKEY:
                        cv2.polylines(
                            img, [np.array(poly_points, np.int32)], True, (0, 0, 0), 1
                        )
                        is_drawing = False
                        poly_points = []
                    else:
                        cv2.polylines(
                            img, [np.array(poly_points, np.int32)], False, (0, 0, 0), 1
                        )

        elif event == cv2.EVENT_MOUSEMOVE and is_drawing and mode == "Polygon":
            temp_img = img.copy()
            temp_points = poly_points + [(x, y)]
            cv2.polylines(
                temp_img, [np.array(temp_points, np.int32)], False, (0, 0, 0), 1
            )
            cv2.imshow("Drawing", temp_img)

    cv2.namedWindow("Drawing")
    cv2.setMouseCallback("Drawing", mouse_callback)

    instructions = f"""Current mode: {mode}
Press M to change mode
Left-click: Draw circle/Start polygon
Shift+Left-click: Continue polygon
Left-click (no Shift): End polygon
Press Enter to save image
Press Esc to exit"""

    while True:
        display_img = img.copy()
        draw_multiline_text(display_img, instructions, (10, 30))
        cv2.imshow("Drawing", display_img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("m"):
            mode = "Polygon" if mode == "Circle" else "Circle"
            instructions = instructions.replace(
                f"Current mode: {('Polygon' if mode == 'Circle' else 'Circle')}",
                f"Current mode: {mode}",
            )
            print(f"Mode changed to: {mode}")
        elif key == 27:  # Esc key
            break
        elif key == 13:  # Enter key
            cv2.imwrite("drawing_resizing/my_drawing.png", img)
            print("Image saved as 'my_drawing.png'")
            break

    cv2.destroyAllWindows()


draw()
