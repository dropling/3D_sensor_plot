try:
    from class_sensor import Sensor
except ImportError:
    from .class_sensor import Sensor

import requests

class Sensor_handler():
    
    def __init__(self, sensor, num_to_average = 5):
        # self.assert_type(sensor, Sensor)
        self.sensor = sensor
        self.list_vals_to_average_num =  num_to_average
        self.list_vals_to_average = []
        
    # Handling sensors: e.g. get data from sensor through local network with mDNS-identification
    
    def get_data_float(self, identification=None, adress_suffix=None, specifier=None):
        
        self.get_data()
        return self.return_average_val()

    def get_data(self, identification="mDNS", adress_suffix=".local", specifier="val"):
        if(identification=="mDNS"):
            self.get_data_mDNS(adress_suffix,specifier)
        else:
            pass
        return None
            
    def get_data_mDNS(self, adress_suffix,specifier):
        
        data = None
        try:
            url = 'http://'+self.sensor.get_name()+adress_suffix+'/'+specifier
            
            data = requests.get(url)
        except:
            pass
        finally:
            self.save_data_to_list_val_to_average(data)
        return None
    
    # Functions for data collection and management
    def save_data_to_list_val_to_average(self, raw_data):
        if(raw_data == None):
            if(len(self.list_vals_to_average)==self.list_vals_to_average_num):
                self.list_vals_to_average.pop()
                self.list_vals_to_average.insert(0, raw_data)
            else:
                self.list_vals_to_average.insert(0, raw_data)
            return
        data = float(raw_data.text)
        if(len(self.list_vals_to_average)==self.list_vals_to_average_num):
            self.list_vals_to_average.pop()
            self.list_vals_to_average.insert(0, data)
        else:
            self.list_vals_to_average.insert(0, data)
        return
    
    def return_average_val(self):
        val = 0
        count = 0
        for value in self.list_vals_to_average:
            if not(value == None):
                val += value
                count += 1
        if(count):
            return val/count
        return None
        
    # Assert functions
    
    def assert_type(self, var, type_):
        assert(isinstance(var, type_)), "Sensor_handler_object: assert_type(self, var, type_): Type Error"
        return