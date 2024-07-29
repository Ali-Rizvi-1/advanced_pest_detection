import argparse
import logging
from datetime import datetime
import os
import time
from typing import Dict, Any

from omegaconf import OmegaConf

from src.image_capture.icm import get_image_capture_module
from src.detection.pest_detector import PestDetector
from src.gps.gps_module import GPSLocator
from utils import prepare_inference_results, save_inference_metadata

# Constants
DEFAULT_CONFIG_PATH = "/Users/alirizvi/Desktop/Ali/advanced_pest_detection/config/config.yaml"
DEFAULT_DATA_ROOT_DIR = "./data/"
DEFAULT_SAVE_DIR = "./records"
DEFAULT_BATCH_SIZE = 16
MAIN_LOOP_INTERVAL = 5  # seconds

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
    image_capture_module = get_image_capture_module(config, args.data_root_dir)
    logging.info("PestDetector, GPSLocator, and ImageCaptureModule initialized")
    
    # Create directories for saving results if they don't exist
    image_save_dir = os.path.join(args.save_dir, "images")
    metadata_save_dir = os.path.join(args.save_dir, "metadata")
    os.makedirs(image_save_dir, exist_ok=True)
    os.makedirs(metadata_save_dir, exist_ok=True)

    while True:
            try:
                should_run_inference, rgb_image_path, thermal_image_path = image_capture_module.run()
                
                if should_run_inference:
                    # Get location information
                    location_info = gps_locator.get_current_location()
                    if not location_info:
                        logging.warning("Unable to retrieve location information")
                        location_info = {}  # Use an empty dict if location info is not available

                    # Perform detections
                    rgb_coordinates = pest_detector.rgb_detect(image=rgb_image_path)
                    thermal_coordinates = pest_detector.thermal_detect(image=thermal_image_path)
                    final_coordinates = pest_detector.combine_coordinates(rgb_coordinates, thermal_coordinates)

                    logging.info(f"RGB detection completed. Coordinates: {rgb_coordinates}")
                    logging.info(f"Thermal detection completed. Coordinates: {thermal_coordinates}")

                    # Save the image with detections
                    saved_image_path = pest_detector.save_detected_image(
                        image=rgb_image_path, 
                        final_coordinates=final_coordinates, 
                        save_dir=image_save_dir
                    )
                    logging.info("Final coordinates displayed on the image")

                    # Prepare inference results
                    inference_results = prepare_inference_results(
                        rgb_coordinates, thermal_coordinates, final_coordinates, 
                        rgb_image_path, thermal_image_path
                    )
                    # Save complete metadata as JSON
                    save_inference_metadata(
                        inference_results, location_info, metadata_save_dir, saved_image_path
                    )

            except Exception as e:
                logging.error(f"Error in main loop: {e}")

            time.sleep(MAIN_LOOP_INTERVAL)

if __name__ == "__main__":
    args = build_args()
    main(args)