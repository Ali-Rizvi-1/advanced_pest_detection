# from src.detection.rgb_detector import RGBDetector
# from src.detection.thermal_detector import ThermalDetector

# class PestDetector:
#     def __init__(self, rgb_model_path, thermal_model_path):
        
#         self.rgb_detector = RGBDetector(rgb_model_path)
#         self.thermal_detector = ThermalDetector(thermal_model_path)
        

#     def rgb_detect(self, image):
#         # Implement YOLOv8 inference for RGB images
#         return self.rgb_detector.detect(image)
    
#     def thermal_detect(self, image):
#         # Implement YOLOv8 inference for Thermal images
#         return self.thermal_detector.detect(image)
    
#     def combine_coordinates(self, rgb_coordinates, thermal_coordinates):
        
#         pass
    
#     def display(self, image, final_coordinates):
#         # display the final coordinates on the image
        
#         pass


import logging
from typing import List, Union

import numpy as np
from src.detection.rgb_detector import RGBDetector
from src.detection.thermal_detector import ThermalDetector

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

    def display(self, image: Union[str, np.ndarray], final_coordinates: List[List[float]]):
        """
        Display the final coordinates on the image.

        :param image: The input image, either as a file path or a NumPy array.
        :param final_coordinates: The coordinates to display on the image.
        """
        print("Displaying final coordinates on the image.")
        try:
            import cv2
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

            cv2.imshow("Detected Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Image displayed with final coordinates.")
        except Exception as e:
            print(f"Error displaying image: {e}")
