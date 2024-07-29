
import logging
from typing import Any, Dict

from src.gps.gps_module import GPSLocator

from datetime import datetime
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def prepare_inference_results(rgb_coordinates: Dict[str, Any], thermal_coordinates: Dict[str, Any], 
                              final_coordinates: Dict[str, Any], rgb_image_path: str, thermal_image_path: str) -> Dict[str, Any]:
    """Prepare inference results dictionary."""
    return {
        'rgb_coordinates': rgb_coordinates,
        'thermal_coordinates': thermal_coordinates,
        'final_coordinates': final_coordinates,
        'rgb_image_path': rgb_image_path,
        'thermal_image_path': thermal_image_path
    }

def save_inference_data(gps_locator: GPSLocator, inference_results: Dict[str, Any], save_dir: str) -> None:
    """Save inference data along with location information."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{save_dir}/inference_result_{timestamp}.json"
    gps_locator.save_inference_data(inference_results, output_path)
    logging.info(f"Inference data saved to {output_path}")