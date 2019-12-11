import json

class Sensor():
    
    def __init__(self, name=None, x=None, y=None, z=None, cal_constant = 0):
        self.name = name
        self.coordinates = [x, y, z]
        self.cal_constant = cal_constant
        
    # Set and get attributes
    
    def set_name(self, name):
        if(name == None or isinstance(name,str)):
            self.name = name
    def get_name(self):
        return self.name
    
    def set_coordinates_by_val(self, x, y, z):
        
        set_value = False
        if(x and self.x != x):
            self.x = x
            set_value = True
        if(y and self.y != y):
            self.y = y
            set_value = True
        if(z and self.z != z):
            self.z = z
            set_value = True
        return set_value
    
    def set_coordinates_by_list(self, coordinates):
        
        self.assert_type(coordinates, list)
        assert(len(coordinates)==3), "Sensor_object: set_coodinates(self, coordinates): coordinate object"
        
        set_value = False
        if(coordinates[0] and self.x != coordinates[0]):
            self.x = coordinates[0]
            set_value = True
        if(coordinates[1] and self.y != coordinates[1]):
            self.y = coordinates[1]
            set_value = True
        if(coordinates[2] and self.z != coordinates[2]):
            self.z = coordinates[2]
            set_value = True
        return set_value
        
    
    
    # Data handling, loading from and saving to json-formated files
    
    def return_coordinates_as_list(self):
        self.assert_coordinates()
        return [self.x, self.y, self.z]

    def set_object_data_from_json(self, data_in_json):
        name = data_in_json.get('name')
        coordinates_as_list = data_in_json.get('coordinates')
        cal_constant = data_in_json.get('cal_constant')
        
        if(name):
            self.name = name
        if(coordinates_as_list):
            self.set_coordinates_by_list(coordinates_as_list)
        if(cal_constant):
            self.cal_constant = cal_constant
    
    def return_object_data_as_json(self):
        self.assert_name()
        self.assert_coordinates()     
        object_data_to_json = {
                "name" : self.name,
                "coordinates" : self.coordinates,
                "cal_constant" : self.cal_constant
                }
        return object_data_to_json
    
    # Property funcitons
    
    @property
    def x(self):
        return self.coordinates[0]
    
    @x.setter
    def x(self, val):
        self.coordinates[0] = val
        
     
    @property
    def y(self):
        return self.coordinates[1]
    
    @y.setter
    def y(self, val):
        self.coordinates[1] = val
     
     
    @property
    def z(self):
        return self.coordinates[2]
    
    @z.setter
    def z(self, val):
        self.coordinates[2] = val
     
    
    # Assert functions
    
    def assert_type(self, var, type_):
        assert(isinstance(var, type_)), "Sensor_object: assert_type(self, var, type_): Type Error"
        return
    
    def assert_coordinates(self):
        for coordinate in self.coordinates:
            assert (coordinate != None),"Sensor_object: assert_coordinates(self): Not all coordinate-values initialized"
        return
    
    def assert_name(self):
        assert(self.name != None), "Sensor_object: assert_name(self): No name specified"
        return