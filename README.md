# Advanced Agricultural Pest Detection and Prediction System

This project implements an advanced system for detecting and predicting agricultural pests using a combination of RGB and thermal imaging, along with environmental parameters.

## Features
- Dual imaging system using RGB and thermal cameras
- YOLOv8-based object detection for both RGB and thermal images
- Fusion of RGB and thermal detections for improved accuracy
- GPS-based location tracking
- Cloud storage integration for data management

## Installation
1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Configure AWS credentials for S3 access

## Usage
Run the main script: `python main.py`

## Configuration
Adjust parameters in `config/config.yaml` to customize the system behavior.

## Testing
Run tests using pytest: `pytest tests/`

## License
[Insert chosen license here]