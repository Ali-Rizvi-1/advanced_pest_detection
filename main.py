# import argparse
# from datetime import datetime
# import logging
# from omegaconf import OmegaConf
# from src.detection.pest_detector import PestDetector
# # from src.image_capture.icm import ImageCaptureMechanism
# from src.gps.gps_module import GPSLocator
# # from src.data_handling.cloud_storage import CloudStorage

# def build_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description="Advanced Pest Detection System")
#     parser.add_argument("--config_path", type=str, default="/Users/alirizvi/Desktop/Ali/advanced_pest_detection/config/config.yaml", help="Path to the configuration file")
#     parser.add_argument("--batch_size", type=int, default=16, help="Batch size for processing")
#     parser.add_argument("--data_root_dir", type=str, default="./data/", help="Root directory for data")
#     parser.add_argument("--save_dir", type=str, default="./records", help="Directory to save output samples")
#     return parser.parse_args()

# def main(args: argparse.Namespace):
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#     logging.info("Starting the pest detection process")

#     # Load configuration
#     config = OmegaConf.load(args.config_path)
#     rgb_model_path = config.rgb_model.path
#     thermal_model_path = config.thermal_model.path
#     logging.info(f"Configuration loaded from {args.config_path}")

#     # Initialize PestDetector module
#     pest_detector = PestDetector(rgb_model_path=rgb_model_path, thermal_model_path=thermal_model_path)
#     logging.info("PestDetector module initialized")
    
#     # Initialize GPSLocator
#     gps_locator = GPSLocator()
#     location_info = gps_locator.get_current_location()
#     if location_info:
#         logging.info("Location information retrieved successfully")
#     else:
#         logging.warning("Unable to retrieve location information")

#     # Detect RGB image
#     rgb_image_path = "/Users/alirizvi/Desktop/Ali/advanced_pest_detection/data/test.jpeg"
#     rgb_coordinates = pest_detector.rgb_detect(image=rgb_image_path)
#     logging.info(f"RGB detection completed. Coordinates: {rgb_coordinates}")

#     # Detect Thermal image
#     thermal_image_path = rgb_image_path  # Adjust this path as needed
#     thermal_coordinates = pest_detector.thermal_detect(image=thermal_image_path)
#     logging.info(f"Thermal detection completed. Coordinates: {thermal_coordinates}")

#     # Combine detection coordinates
#     final_coordinates = pest_detector.combine_coordinates(rgb_coordinates, thermal_coordinates)
#     # logging.info(f"Combined coordinates: {final_coordinates}")

#     # Display final coordinates on the image
#     pest_detector.display(image=rgb_image_path, final_coordinates=final_coordinates)
#     logging.info("Final coordinates displayed on the image")
    
#     # Prepare inference results
#     inference_results = {
#         'rgb_coordinates': rgb_coordinates,
#         'thermal_coordinates': thermal_coordinates,
#         'final_coordinates': final_coordinates,
#         'rgb_image_path': rgb_image_path,
#         'thermal_image_path': thermal_image_path
#     }

#     # Save inference data along with location information
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_path = f"{args.save_dir}/inference_result_{timestamp}.json"
#     gps_locator.save_inference_data(inference_results, output_path)
#     logging.info(f"Inference data saved to {output_path}")


# if __name__ == "__main__":
#     args = build_args()
#     main(args)


import argparse
import logging
from datetime import datetime
from typing import Dict, Any

from omegaconf import OmegaConf

from src.detection.pest_detector import PestDetector
from src.gps.gps_module import GPSLocator
from utils import prepare_inference_results, save_inference_data

# Constants
DEFAULT_CONFIG_PATH = "/Users/alirizvi/Desktop/Ali/advanced_pest_detection/config/config.yaml"
DEFAULT_DATA_ROOT_DIR = "./data/"
DEFAULT_SAVE_DIR = "./records"
DEFAULT_BATCH_SIZE = 16

def build_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(description="Advanced Pest Detection System")
    parser.add_argument("--config_path", type=str, default=DEFAULT_CONFIG_PATH, help="Path to the configuration file")
    parser.add_argument("--batch_size", type=int, default=DEFAULT_BATCH_SIZE, help="Batch size for processing")
    parser.add_argument("--data_root_dir", type=str, default=DEFAULT_DATA_ROOT_DIR, help="Root directory for data")
    parser.add_argument("--save_dir", type=str, default=DEFAULT_SAVE_DIR, help="Directory to save output samples")
    return parser.parse_args()

def main(args: argparse.Namespace) -> None:
    """Main function to run the pest detection process."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting the pest detection process")

    # Load configuration
    config = OmegaConf.load(args.config_path)
    rgb_model_path = config.rgb_model.path
    thermal_model_path = config.thermal_model.path
    logging.info(f"Configuration loaded from {args.config_path}")

    # Initialize modules
    pest_detector = PestDetector(rgb_model_path=rgb_model_path, thermal_model_path=thermal_model_path)
    gps_locator = GPSLocator()
    logging.info("PestDetector and GPSLocator modules initialized")

    # Get location information
    location_info = gps_locator.get_current_location()
    if location_info:
        logging.info("Location information retrieved successfully")
    else:
        logging.warning("Unable to retrieve location information")

    # Perform detections
    rgb_image_path = f"{args.data_root_dir}/test.jpeg"
    thermal_image_path = rgb_image_path  # Adjust this path as needed

    rgb_coordinates = pest_detector.rgb_detect(image=rgb_image_path)
    thermal_coordinates = pest_detector.thermal_detect(image=thermal_image_path)
    final_coordinates = pest_detector.combine_coordinates(rgb_coordinates, thermal_coordinates)

    logging.info(f"RGB detection completed. Coordinates: {rgb_coordinates}")
    logging.info(f"Thermal detection completed. Coordinates: {thermal_coordinates}")

    # Display final coordinates on the image
    pest_detector.display(image=rgb_image_path, final_coordinates=final_coordinates)
    logging.info("Final coordinates displayed on the image")

    # Prepare and save inference results
    inference_results = prepare_inference_results(rgb_coordinates, thermal_coordinates, final_coordinates, rgb_image_path, thermal_image_path)
    save_inference_data(gps_locator, inference_results, args.save_dir)

if __name__ == "__main__":
    args = build_args()
    main(args)