import yaml
from datetime import datetime

class SepticTankHealthChecker:
    def __init__(self, config_file, log_file):
        with open(config_file, 'r') as file:
            self.data = yaml.safe_load(file)
        self.issues = []
        self.log_file_path = log_file
        self.log_file = open(self.log_file_path, "a")
        
    def __del__(self):
        self.log_file.close()

    def log_issue(self, msg_type, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}\t{msg_type}:\t{message}\n"
        self.log_file.write(log_entry)
        self.issues.append(message)

    def check_water_level(self):
        tank_depth_ft = self.data['config']['depth']
        water_level_ft = self.data['data']['water-level']
        water_level_from_top_in = (tank_depth_ft - water_level_ft) * 12
        
        if not (8 <= water_level_from_top_in <= 12):
            self.log_issue("Warning", f"Water Level is {water_level_from_top_in:.2f} inches from top. Ideal range: 8-12 inches.")

    def check_temperature(self):
        temperature = self.data['data']['temperature']
        if not (20 <= temperature <= 40):
            self.log_issue("Warning", "Temperature is out of optimal range 20-40°C.")

    def check_soil_moisture(self):
        soil_type = self.data['config']['soil-type']
        moisture = self.data['data']['soil-moisture']
        soil_moisture_ranges = {
            'sandy': (5, 12),
            'loam': (10, 30),
            'clay': (25, 40),
        }
        min_moisture, max_moisture = soil_moisture_ranges.get(soil_type, (0, 100))
        if not (min_moisture <= moisture <= max_moisture):
            self.log_issue("Warning", f"Soil Moisture for {soil_type.capitalize()} Soil is out of optimal range {min_moisture}-{max_moisture}%.")

    def check_pH(self):
        ph = self.data['data']['ph']
        if not (6.5 <= ph <= 8.5):
            self.log_issue("Warning", "pH is out of optimal range 6.5-8.5.")

    def check_gases(self):
        methane = self.data['data']['methane']
        hydrogen_sulfide = self.data['data']['hydrogen-sulfide']
        ammonia = self.data['data']['ammonia']
        
        if methane >= 1000:
            self.log_issue("Error", "Methane Levels are above safe levels (1000 ppm).")
        if hydrogen_sulfide >= 20:
            self.log_issue("Error", "Hydrogen Sulfide Levels are above safe levels (20 ppm).")
        if ammonia >= 50:
            self.log_issue("Error", "Ammonia Levels are above safe levels (50 ppm).")

    def check_sludge_depth(self):
        sludge_depth = self.data['data']['sludge-depth']
        tank_depth_ft = self.data['config']['depth']
        if sludge_depth >= (tank_depth_ft / 3):
            self.log_issue("Warning", "Sludge Depth exceeds 1/3 of tank depth.")
        
    def check_health(self):
        self.check_water_level()
        self.check_temperature()
        self.check_soil_moisture()
        self.check_pH()
        self.check_gases()
        self.check_sludge_depth()

        if self.issues:
            print("Septic Tank Health Issues Identified:")
            for issue in self.issues:
                print(f"- {issue}")
        else:
            print("Septic Tank is Healthy!")


checker = SepticTankHealthChecker('config.yaml', 'log.txt')
checker.check_health()
del checker