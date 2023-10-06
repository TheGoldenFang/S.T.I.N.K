from ruamel.yaml import YAML

class SensorDataReader:
    SENSOR_PINS = {
        'water-level': 17,
        'sludge-depth': 18,
        'temperature': 27,
        'soil-moisture': 22,
        'ph': 23,
        'methane': 24,
        'hydrogen-sulfide': 25,
        'ammonia': 4
    }

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True  
        self.yaml.width = 4096  
        self.yaml.indent(mapping=2, sequence=4, offset=2) 
        self.data = self._load_yaml_data()
    
    def _load_yaml_data(self):
        with open(self.config_file_path, 'r') as file:
            return self.yaml.load(file)
    
    def _save_yaml_data(self):
        with open(self.config_file_path, 'w') as file:
            self.yaml.dump(self.data, file)
    
    def read_sensor(self, pin):
        print(f"Reading data from pin: {pin}")
        return 10  # This is a stub. Actual reading mechanism should replace this.

    def update_sensor_data(self):
        for sensor, pin in self.SENSOR_PINS.items():
            sensor_value = self.read_sensor(pin)
            self.data['data'][sensor] = sensor_value
    
    def sync_data(self):
        self.update_sensor_data()
        self._save_yaml_data()

config_file_path = 'config.yaml'  
sensor_data_reader = SensorDataReader(config_file_path)
sensor_data_reader.sync_data()
