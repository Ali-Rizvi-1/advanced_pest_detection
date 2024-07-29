import requests
from datetime import datetime
import json

class GPSLocator:
    def __init__(self):
        self.lat = None
        self.long = None
        self.city = None
        self.state = None
        self.country = None
        self.ip = None
        self.timezone = None
        self.timestamp = None

    def get_location_info(self):
        try:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            
            loc = data['loc'].split(',')
            self.lat, self.long = float(loc[0]), float(loc[1])
            self.city = data.get('city', 'Unknown')
            self.state = data.get('region', 'Unknown')
            self.country = data.get('country', 'Unknown')
            self.ip = data.get('ip', 'Unknown')
            self.timezone = data.get('timezone', 'Unknown')
            self.timestamp = datetime.now().isoformat()

            return {
                'latitude': self.lat,
                'longitude': self.long,
                'city': self.city,
                'state': self.state,
                'country': self.country,
                'ip': self.ip,
                'timezone': self.timezone,
                'timestamp': self.timestamp
            }
        except:
            print("Internet Not available or error in fetching location data")
            return None

    def get_current_location(self):
        location_info = self.get_location_info()
        if location_info:
            print(f"Location Info:")
            print(json.dumps(location_info, indent=2))
            return location_info
        else:
            return None

    def save_inference_data(self, inference_results, output_path):
        location_info = self.get_location_info()
        if location_info is None:
            location_info = {}

        data_to_save = {
            'location_info': location_info,
            'inference_results': inference_results
        }

        with open(output_path, 'w') as f:
            json.dump(data_to_save, f, indent=2)