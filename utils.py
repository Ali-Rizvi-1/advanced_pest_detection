
import logging
from typing import Any, Dict

from src.gps.gps_module import GPSLocator

from datetime import datetime

import json
import os
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

def save_inference_metadata(inference_results: dict, location_info: dict, save_dir: str, image_path: str) -> str:
    """
    Save the complete metadata of the inference as a JSON file.

    :param inference_results: Dictionary containing inference results.
    :param location_info: Dictionary containing location information.
    :param save_dir: Directory to save the JSON file.
    :param image_path: Path to the saved image with detections.
    :return: Path to the saved JSON file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metadata = {
        "timestamp": timestamp,
        "location_info": location_info,
        "inference_results": inference_results,
        "detected_image_path": image_path
    }

    json_filename = f"inference_metadata_{timestamp}.json"
    json_path = os.path.join(save_dir, json_filename)

    with open(json_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    print(f"Inference metadata saved to: {json_path}")
    return json_path