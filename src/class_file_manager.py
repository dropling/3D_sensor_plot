import json

try:
    from class_point import Point
except ImportError:
    from .class_point import Point


try:
    from class_sensor import Sensor
except ImportError:
    from .class_sensor import Sensor

class File_Manager():
    # attributes
    # mode = str
    mode = None # in 'r' read or 'w' write
    # file = str
    file = None
    # object_type = str
    object_type = None
    # data = dict
    data = None
    
    def __init__(self, mode, file=None, object_type = None):
        if (mode == 'w') or (mode == 'r'):
            raise Exception
        self.file = file
        self.object_type = object_type
        if(mode == "r"):
            self.load_data()
        
    def set_file(self, file):
        self.file = file
        
    def set_object_type(self, object_type):
        self.object_type = object_type
        
    def return_objects_list(self):
        if(self.object_type == 'Sensor'):
            return self.return_sensors_list()
        elif(self.object_type == 'Point'):
            return self.return_points_list()
        elif(self.object_type == None):
            return None
        else:
            return None
        
    def return_sensors_list(self):
#        sensor-file-structure:
#            {'sensor_1':{'name':'sth','coordinates':list,'cal_constant':float},
#             'sensor_2':{'name':'sth','coordinates':list,'cal_constant':float},
#             'sensor_3':{'name':'sth','coordinates':list,'cal_constant':float},}
        if(self.data == None):
            return
        sensors = []
        for dict_item in self.data:
            sensors.append(dict_item.value)
        return sensors
    
    def return_points_list(self):
#        points-file-structure:
#            {'point_1':{'ID':'sth','coordinates':list,'_set_proximity':list},
#             'point_2':{'ID':'sth','coordinates':list,'_set_proximity':list},
#             'point_3':{'ID':'sth','coordinates':list,'_set_proximity':list}}
        if(self.data == None):
            return
        points = []
        for dict_item in self.data:
            points.append(dict_item.value)
        return points
    
    def load_data(self):
        if not(self.mode == 'r'):
            return
        if(self.file == None):
            return False
        f = None
        try:
            f = open(self.file)
        except:
            return False
        json_content = f.read()
        self.data = json.load(json_content)
        return True
    
    def return_data_as_dict(self):
        if(isinstance(self.data,dict)):
            return self.data # super careful here, shares a reference!
     
        
    def save_data(self,json_data):
        if not(self.mode == 'w'):
            return
        if not(isinstance(json_data,dict)):
            return False
        f = None
        try:
            f = open(self.file)
        except:
            return False
        json.dump(json_data, f)
        return True