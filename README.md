# Advanced Agricultural Pest Detection and Prediction System

## Project Overview

This project implements an advanced system for detecting and predicting agricultural pests using a combination of RGB and thermal imaging, along with environmental parameters. It utilizes state-of-the-art object detection models and integrates GPS location tracking for comprehensive pest monitoring in agricultural settings.

## Features

- Dual imaging system using RGB and thermal cameras
- YOLOv8-based object detection for both RGB and thermal images
- Fusion of RGB and thermal detections for improved accuracy
- GPS-based location tracking
- Cloud storage integration for data management
- Configurable settings via YAML configuration file

## Project Structure

```
.
├── config
│   └── config.yaml
├── data
│   └── test.jpeg
├── main.py
├── models
│   └── yolov8n.pt
├── records
│   └── [inference results]
├── requirements.txt
├── src
│   ├── data_handling
│   ├── detection
│   ├── fusion
│   ├── gps
│   └── image_capture
├── tests
└── utils.py
```
## Installation

1. Clone this repository:
```bash
git clone https://github.com/Ali-Rizvi-1/advanced_pest_detection.git
cd advanced_pest_detection
```
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Configure AWS credentials for S3 access (if using cloud storage)

## Usage

Run the main script with optional arguments:
python main.py [--config_path CONFIG_PATH] [--batch_size BATCH_SIZE] [--data_root_dir DATA_ROOT_DIR] [--save_dir SAVE_DIR]
Copy
Arguments:
- `--config_path`: Path to the configuration file (default: `./config/config.yaml`)
- `--batch_size`: Batch size for processing (default: 16)
- `--data_root_dir`: Root directory for input data (default: `./data/`)
- `--save_dir`: Directory to save output results (default: `./records`)

## Configuration

Adjust parameters in `config/config.yaml` to customize the system behavior. Key configurations include:

- RGB and thermal model paths
- Detection confidence thresholds
- Cloud storage settings

## Modules

- **PestDetector**: Combines RGB and thermal detections
- **RGBDetector** and **ThermalDetector**: Perform YOLO-based object detection
- **GPSLocator**: Retrieves and manages location information
- **Fusion Module**: Combines detections from multiple sources (to be implemented)

## Testing

Run tests using pytest:
pytest tests/
Copy

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. See the LICENSE file for details.

## Contact

- Syed Muhammad Ali Rizvi - alirizvi277.ar@gmail.com
- Syed Muhammad Hussain
- Samiya Ali Zaidi
- Huzaifah Tariq Ahmed

Project Link: [https://github.com/Ali-Rizvi-1/advanced_pest_detection](https://github.com/Ali-Rizvi-1/advanced_pest_detection)