import cv2
import numpy as np
import os
from pathlib import Path

INPUT_DIR = os.path.join(os.getcwd(), "snack/org")
OUTPUT_DIR = os.path.join(os.getcwd(), "snack/dist")
TARGET_SIZE = (224, 224)


class ImageAugmentor:
    def rotate(self, image, angle):
        height, width = image.shape[:2]
        center = (width // 2, height // 2)

        diagonal = int(np.ceil(np.sqrt(width**2 + height**2)))

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotation_matrix[0, 2] += (diagonal - width) // 2
        rotation_matrix[1, 2] += (diagonal - height) // 2

        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (diagonal, diagonal),
            cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT,
        )

        start_x = (diagonal - width) // 2
        start_y = (diagonal - height) // 2
        rotated = rotated[start_y : start_y + height, start_x : start_x + width]

        return rotated

    def flip(self, image, direction="horizontal"):
        if direction == "horizontal":
            return cv2.flip(image, 1)
        elif direction == "vertical":
            return cv2.flip(image, 0)
        else:
            return cv2.flip(image, -1)

    def scale(self, image, factor):
        height, width = image.shape[:2]
        new_height, new_width = int(height * factor), int(width * factor)
        scaled = cv2.resize(
            image, (new_width, new_height), interpolation=cv2.INTER_LINEAR
        )

        if factor > 1:
            start_y = (new_height - height) // 2
            start_x = (new_width - width) // 2
            scaled = scaled[start_y : start_y + height, start_x : start_x + width]
        else:
            pad_y = (height - new_height) // 2
            pad_x = (width - new_width) // 2
            scaled = cv2.copyMakeBorder(
                scaled,
                pad_y,
                height - new_height - pad_y,
                pad_x,
                width - new_width - pad_x,
                cv2.BORDER_REFLECT,
            )

        return scaled

    def add_noise(self, image, level=25):
        noise = np.random.normal(0, level, image.shape).astype(np.uint8)
        return np.clip(image.astype(np.int32) + noise, 0, 255).astype(np.uint8)

    def blur(self, image, kernel_size=3):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def adjust_brightness(self, image, factor):
        return cv2.convertScaleAbs(image, alpha=factor, beta=0)

    def adjust_contrast(self, image, factor):
        return cv2.addWeighted(image, factor, image, 0, 0)


def process_images(input_dir, output_dir):
    augmentor = ImageAugmentor()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for img_file in input_path.glob("*"):
        image = cv2.imread(str(img_file))
        if image is None:
            print("Unable to read.")
            continue

        image = cv2.resize(image, TARGET_SIZE)
        base_name = img_file.stem

        cv2.imwrite(
            str(output_path / f"{base_name}_rotated_15.jpg"),
            augmentor.rotate(image, 15),
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_flipped_h.jpg"),
            augmentor.flip(image, "horizontal"),
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_scaled_1.5.jpg"),
            augmentor.scale(image, 1.5),
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_blurred.jpg"), augmentor.blur(image, 3)
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_noisy.jpg"), augmentor.add_noise(image, 20)
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_bright.jpg"),
            augmentor.adjust_brightness(image, 1.2),
        )
        cv2.imwrite(
            str(output_path / f"{base_name}_contrast.jpg"),
            augmentor.adjust_contrast(image, 1.2),
        )


def main():
    process_images(INPUT_DIR, OUTPUT_DIR)


if __name__ == "__main__":
    main()
