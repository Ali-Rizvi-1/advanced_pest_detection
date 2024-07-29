from ultralytics import YOLO
from typing import List, Union
import numpy as np
import cv2

class RGBDetector:
    def __init__(self, model_path: str, conf_threshold: float = 0.3):
        """
        Initialize the RGBDetector with a YOLO model.

        :param model_path: Path to the YOLO model file.
        :param conf_threshold: Confidence threshold for detections.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        print(f"RGB Model loaded from {model_path} with confidence threshold {conf_threshold}")

    def _load_image(self, image: Union[str, np.ndarray]) -> np.ndarray:
        """
        Load an image from a file path or directly use an image array.

        :param image: The input image, either as a file path or a NumPy array.
        :return: The image as a NumPy array.
        """
        if isinstance(image, str):
            print(f"Loading image from path: {image}")
            image = cv2.imread(image)
            if image is None:
                raise ValueError(f"Image at path {image} could not be loaded.")
        else:
            print("Using provided image array.")
        return image

    def detect(self, image: Union[str, np.ndarray]) -> List[List[float]]:
        """
        Perform object detection on an RGB image using YOLO.

        :param image: The input image, either as a file path or a NumPy array.
        :return: A list of bounding box coordinates in xywhn format.
        """
        try:
            image = self._load_image(image)
            print("Starting RGB detection...")
            result_rgb = self.model.predict(source=image, conf=self.conf_threshold)
            boxes_rgb = result_rgb[0].boxes.xywhn

            rgb_coordinates = [box.tolist() for box in boxes_rgb]
            print(f"RGB Detection completed. Found {len(rgb_coordinates)} objects.")

            return rgb_coordinates
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
