import cv2
import numpy as np
from pathlib import Path
from functools import partial


INPUT_DIR = Path.cwd() / "snack" / "org"
OUTPUT_DIR = Path.cwd() / "snack" / "dist"
TARGET_SIZE = (224, 224)


class ImageAugmentor:
    @staticmethod
    def rotate(image: np.ndarray, angle: float) -> np.ndarray:
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

    @staticmethod
    def flip(image: np.ndarray, direction: str = "horizontal") -> np.ndarray:
        codes = {"horizontal": 1, "vertical": 0, "both": -1}
        return cv2.flip(image, codes.get(direction, 1))

    @staticmethod
    def scale(image: np.ndarray, factor: float) -> np.ndarray:
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

    @staticmethod
    def add_noise(image: np.ndarray, level: int = 25):
        noise = np.random.normal(0, level, image.shape).astype(np.uint8)
        return np.clip(image.astype(np.int32) + noise, 0, 255).astype(np.uint8)

    @staticmethod
    def blur(image: np.ndarray, kernel_size: int = 3):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    @staticmethod
    def adjust_brightness(image: np.ndarray, factor: float):
        return cv2.convertScaleAbs(image, alpha=factor, beta=0)

    @staticmethod
    def adjust_contrast(image: np.ndarray, factor: float):
        return cv2.addWeighted(image, factor, image, 0, 0)


def process_images(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    augmentor = ImageAugmentor()

    augmentations = [
        ("rotated_15", partial(augmentor.rotate, angle=15)),
        ("flipped_h", partial(augmentor.flip, direction="horizontal")),
        ("scaled_1_5", partial(augmentor.scale, factor=1.5)),
        ("blurred", partial(augmentor.blur, kernel_size=3)),
        ("noisy", partial(augmentor.add_noise, level=20)),
        ("bright", partial(augmentor.adjust_brightness, factor=2)),
        ("contrast", partial(augmentor.adjust_contrast, factor=1.2)),
    ]

    for img_file in input_dir.glob("*"):
        image = cv2.imread(str(img_file))
        if image is None:
            print("Unable to read.")
            continue

        image = cv2.resize(image, TARGET_SIZE)
        base_name = img_file.stem

        for name, func in augmentations:
            output_path = output_dir / f"{base_name}_{name}.jpg"
            cv2.imwrite(str(output_path), func(image))


def main():
    process_images(INPUT_DIR, OUTPUT_DIR)


if __name__ == "__main__":
    main()
