# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 00:18:26 2019

@author: marku
"""
import json

# class point definition
class Point():
    ID = str() # should save str()
    coordinates = list() # should save float()s
    _set_proximity = set() # should save str()s
    
    def __init__(self, ID, x, y, z):
        self.ID = ID
        self.coordinates = [x,y,z]
        
    
    def adjacent_points_add(self, data=None): # gets a piece of data and reroutes it into the appropriate function
        if(data==None):
            return False
        if(isinstance(data,list)):
            for item in data: # check if all the content is string
                if not(isinstance(item,(str,Point))):
                    return False
            self.adjacent_points_add_from_list(data) # call set-function for list
            return True
        elif(isinstance(data,str)):
            self.adjacent_point_add_from_str(data) # call set-function for string
            return True
        elif(isinstance(data,Point)):
            self.adjacent_point_add_from_Point(data) # call set-function for Point
        else:
            pass
        return False

    def adjacent_points_add_from_list(self, data_of_type_list): # gets a list of strings and sets them individually for now.
                                                                # reasoning is problems detected in the initialization of empty sets and their further usage
                                                                # cause the memory adress of sets in multiple simultaniously initialized points were identical
        for item in data_of_type_list:
            if(isinstance(item,str)):
                self.adjacent_point_add_from_str(item) # call single point setter function from str
            if(isinstance(item,Point)):
                self.adjacent_point_add_from_Point(item) # call single point setter function from Point
        return

    def adjacent_point_add_from_str(self, data_of_type_str): # Single point setter function
        if not(len(self._set_proximity)==0):
            self._set_proximity.add(data_of_type_str)
        elif(len(self._set_proximity)==0):
            self._set_proximity = {data_of_type_str} # if set is empty so far, sets it anew with a newly initialized
        else:
            print("class_point: adjacent_point_add_from_str: somthing went horribly wrong")
        return
    
    def adjacent_point_add_from_Point(self, data_of_type_Point): # Single point setter function
        if not(len(self._set_proximity)==0):
            self._set_proximity.add(data_of_type_Point.ID)
        elif(len(self._set_proximity)==0):
            self._set_proximity = {data_of_type_Point.ID} # if set is empty so far, sets it anew with a newly initialized
        else:
            print("class_point: adjacent_point_add_from_str: somthing went horribly wrong")
        return

    def return_adjacent_points(self):
        return self._set_proximity.copy()
    
    
    def set_coordinates_by_list(self, coordinates):
        if not(isinstance(coordinates,list)):
            return False
        assert(len(coordinates)==3), "Point_object: set_coodinates(self, coordinates): coordinate object"
        
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
    
    def return_coordinates(self):
        return self.coordinates.copy()

    # Data management setter and save functions for json-format data handling
    
    def set_object_data_from_json(self, data_in_json):
        ID = data_in_json.get('ID')
        coordinates_as_list = data_in_json.get('coordinates')
        _set_proximity = data_in_json.get('_set_proximity') # data in form list
        
        if(ID):
            self.ID = ID
        if(coordinates_as_list):
            self.set_coordinates_by_list(coordinates_as_list)
        if(_set_proximity):
            self.adjacent_points_add(_set_proximity)
    
    def return_object_data_as_json(self):
        object_data_to_json = {
                "ID" : self.ID,
                "coordinates" : self.coordinates,
                "_set_proximity" : list(self._set_proximity)
                }
        return json.dumps(object_data_to_json)

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
        