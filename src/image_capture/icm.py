import time
import os
from typing import Tuple, Optional

class ImageCaptureModule:
    def __init__(self, data_root_dir: str, capture_interval: int = 60):
        self.data_root_dir = data_root_dir
        self.capture_interval = capture_interval
        self.last_capture_time = 0
        self.image_index = 0
        # self.image_files = self._get_image_files()
        self.test_image = self._get_test_image()


    # def _get_image_files(self):
    #     """Get a list of image files in the data directory."""
    #     return [f for f in os.listdir(self.data_root_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    def _get_test_image(self):
        """Get the test image from the data directory."""
        image_files = [f for f in os.listdir(self.data_root_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            raise ValueError(f"No image files found in {self.data_root_dir}")
        return os.path.join(self.data_root_dir, image_files[0])


    def is_capture_time(self) -> bool:
        """Check if it's time to capture new images."""
        current_time = time.time()
        if current_time - self.last_capture_time >= self.capture_interval:
            return True
        return False

    # def capture_images(self) -> Tuple[Optional[str], Optional[str]]:
    #     """Simulate capturing both RGB and thermal images."""
    #     if not self.image_files:
    #         return None, None
        
    #     image_file = self.image_files[self.image_index % len(self.image_files)]
    #     rgb_image_path = os.path.join(self.data_root_dir, image_file)
    #     thermal_image_path = rgb_image_path  # For simulation, use the same image for thermal

    #     self.image_index += 1
    #     self.last_capture_time = time.time()
    #     return rgb_image_path, thermal_image_path
    
    def capture_images(self) -> Tuple[str, str]:
        """Simulate capturing both RGB and thermal images."""
        self.last_capture_time = time.time()
        return self.test_image, self.test_image  # Use the same image for both RGB and thermal


    def run(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """Main method to run the image capture process."""
        if self.is_capture_time():
            rgb_image, thermal_image = self.capture_images()
            if rgb_image and thermal_image:
                return True, rgb_image, thermal_image
        return False, None, None

def get_image_capture_module(config, data_root_dir: str) -> ImageCaptureModule:
    """Factory function to create and return an ImageCaptureModule instance."""
    capture_interval = config.image_capture.interval
    return ImageCaptureModule(data_root_dir, capture_interval)