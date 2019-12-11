import json

try:
    from class_point import Point
except ImportError:
    from .class_point import Point


try:
    from class_sensor import Sensor
except ImportError:
    from .class_sensor import Sensor

class File_manager():
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
        if not (mode == 'w') and not (mode == 'r'):
            raise Exception
        self.file = file
        self.object_type = object_type
        self.mode = mode
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
        for key in self.data:
            dict_item = self.data[key]
            x,y,z = dict_item['coordinates']
            sensor = Sensor(dict_item['name'], x, y, z, dict_item['cal_constant'])
            sensors.append(sensor)
        return sensors
    
    
    def return_points_list(self):
#        points-file-structure:
#            {'point_1':{'ID':'sth','coordinates':list,'_set_proximity':list},
#             'point_2':{'ID':'sth','coordinates':list,'_set_proximity':list},
#             'point_3':{'ID':'sth','coordinates':list,'_set_proximity':list}}
        if(self.data == None):
            return
        points = []
        for key in self.data:
            dict_item = self.data[key]
            x,y,z = dict_item['coordinates']
            point = Point(dict_item['ID'], x, y, z)
            point.adjacent_points_add(dict_item['_set_proximity'])
            points.append(point)
        return points
    
    def load_data(self):
        if not(self.mode == 'r'):
            return
        if(self.file == None):
            return False
        f = None
        try:
            f = open(self.file,'r')
        except:
            return False
        if(f.mode == 'r'):
            json_content = f.read()
            self.data = json.loads(json_content)
            return True
        return False
    
    def return_data_as_dict(self):
        if(isinstance(self.data,dict)):
            return self.data # super careful here, shares a reference!
     
    def save_points(self, points):
        json_data={}
        count = 0
        for point in points:
            json_data.update({"point_"+str(count):point.return_object_data_as_json().copy()})
            count+=1
        self.save_data(json_data)
    
    def save_sensors(self, sensors):
        json_data={}
        count = 0
        for sensor in sensors:
            json_data.update({"sensor_"+str(count):sensor.return_object_data_as_json().copy()})
            count+=1
        self.save_data(json_data)
        
    def save_data(self,json_data):
        if not(self.mode == 'w'):
            print("Mode wrong")
            return False
        if not(isinstance(json_data,dict)):
            print("data type wrong")
            return False
        f = None
        try:
            f = open(self.file,"w+")
        except:
            print(False)
            return False
        json.dump(json_data, f)
        print(True)
        return True