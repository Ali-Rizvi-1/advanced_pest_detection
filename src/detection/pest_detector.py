import os
from typing import List, Union

import cv2
import numpy as np
from src.detection.rgb_detector import RGBDetector
from src.detection.thermal_detector import ThermalDetector

from datetime import datetime

class PestDetector:
    def __init__(self, rgb_model_path: str, thermal_model_path: str):
        """
        Initialize the PestDetector with paths to the RGB and Thermal models.

        :param rgb_model_path: Path to the RGB YOLO model.
        :param thermal_model_path: Path to the Thermal YOLO model.
        """
        self.rgb_detector = RGBDetector(rgb_model_path)
        self.thermal_detector = ThermalDetector(thermal_model_path)
        print("PestDetector initialized with RGB and Thermal models.")

    def rgb_detect(self, image: Union[str, np.ndarray]) -> List[List[float]]:
        """
        Perform inference for RGB images.

        :param image: The input RGB image, either as a file path or a NumPy array.
        :return: A list of bounding box coordinates.
        """

        return self.rgb_detector.detect(image)

    def thermal_detect(self, image: Union[str, np.ndarray]) -> List[List[float]]:
        """
        Perform YOLOv8 inference for Thermal images.

        :param image: The input Thermal image, either as a file path or a NumPy array.
        :return: A list of bounding box coordinates.
        """
        return self.thermal_detector.detect(image)

    def combine_coordinates(self, rgb_coordinates: List[List[float]], thermal_coordinates: List[List[float]]) -> List[List[float]]:
        """
        Combine detection coordinates from RGB and Thermal images.

        :param rgb_coordinates: Coordinates from RGB detection.
        :param thermal_coordinates: Coordinates from Thermal detection.
        :return: Combined coordinates.
        """
        print("Combining coordinates from RGB and Thermal detections.")
        # Placeholder implementation, should be replaced with actual logic
        # Convert coordinates to tuples to use in a set for uniqueness
        all_coordinates = set(tuple(coord) for coord in rgb_coordinates + thermal_coordinates)
        combined_coordinates = [list(coord) for coord in all_coordinates]
        # combined_coordinates = rgb_coordinates + thermal_coordinates
        print(f"Combined coordinates: {combined_coordinates}")
        return combined_coordinates
    
    def save_detected_image(self, image: Union[str, np.ndarray], final_coordinates: List[List[float]], save_dir: str):
        """
        Save the image with final coordinates drawn on it.

        :param image: The input image, either as a file path or a NumPy array.
        :param final_coordinates: The coordinates to display on the image.
        :param save_dir: Directory to save the output image.
        """
        print("Saving image with final coordinates.")
        try:
            if isinstance(image, str):
                image = cv2.imread(image)
                if image is None:
                    raise ValueError(f"Image at path {image} could not be loaded.")
            
            height, width = image.shape[:2]
            
            for coord in final_coordinates:
                # YOLO format is [x_center, y_center, width, height] normalized
                x_center, y_center, w, h = coord
                
                # Convert normalized coordinates to pixel values
                x = int((x_center - w/2) * width)
                y = int((y_center - h/2) * height)
                w = int(w * width)
                h = int(h * height)
                
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Optionally, add text with coordinates
                label = f"({x_center:.2f}, {y_center:.2f})"
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(save_dir, f"detected_image_{timestamp}.jpg")
            cv2.imwrite(save_path, image)
            print(f"Image saved with final coordinates at: {save_path}")
        except Exception as e:
            print(f"Error processing image: {e}")