import cv2
import numpy as np
import os


# utility
def get_full_path(folder, file):
    base = os.getcwd()
    return os.path.join(base, folder, file)


class ImageLabeller:
    def __init__(self, winname, path):
        self.img = cv2.imread(path)
        self.winname = winname
        self.path = path

        if self.img is None:
            raise ValueError("Failed to load a image")

        # 초기값 세팅
        self.pt_list = []
        self.current_rect = None
        self.drawing = False

        # cv2 세팅
        cv2.namedWindow(winname)
        cv2.setMouseCallback(winname, self.on_mouse_callback)

    def on_mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # 그리기 시작 - start값 세팅
            self.drawing = True
            self.current_rect = [(x, y), (x, y)]
        elif event == cv2.EVENT_MOUSEMOVE:
            # 1. is drawing 드로잉이 시작되었을 때만 end포인트 업데이트
            # 2. current_rect값을 가지고 드래그 사각형 그리기
            if self.drawing:
                self.current_rect[1] = (x, y)
                self.draw_rect()
        elif event == cv2.EVENT_LBUTTONUP:
            # 마우스 업하면 저장할 사각형을 그린것이므로
            # (start와 end포인트 값이 다르면) pt_list에 값 추가(append)
            self.drawing = False
            if self.current_rect[0] != self.current_rect[1]:
                self.pt_list.append(self.current_rect)
            # 드로잉이 끝났으므로 current_rect값을 리셋하고, 현재까지의 사각형을 그린다.
            self.current_rect = None
            self.draw_rect()

    def draw_rect(self):
        # 이미지를 카피
        img_copy = self.img.copy()

        for start, end in self.pt_list:
            cv2.rectangle(img_copy, start, end, (0, 255, 0), 2)

        # current rectangle도 그린다.
        if self.current_rect:
            cv2.rectangle(
                img_copy, self.current_rect[0], self.current_rect[1], (0, 255, 255), 2
            )

        cv2.imshow(self.winname, img_copy)

    def clear(self):
        self.pt_list.clear()
        # 저장된 포인트들을 지우고 빈 값으로 그려서 업데이트
        self.draw_rect()

    def save_file(self):
        file_name, _ = os.path.splitext(self.path)

        with open(f"{file_name}.txt", "w") as f:
            f.write(f"points: {self.pt_list}")
        print(f"Saved as {file_name}.txt")

    def run(self):
        # cv2 초기 진입지점 - 이미지 그리기 및 waitKey핸들링
        cv2.imshow(self.winname, self.img)

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break
            if key == ord("s"):
                self.save_file()
            if key == ord("c"):
                self.clear()

        cv2.destroyAllWindows()


def main():
    DIR = "image_labeller/img"
    FILE_NAME = "cat1.jpg"

    labeller = ImageLabeller("Labeller", get_full_path(DIR, FILE_NAME))
    labeller.run()


main()
