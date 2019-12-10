#import statements
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from scipy.interpolate import griddata
import numpy as np
from matplotlib.figure import Figure
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

try:
    from class_point import Point
except ImportError:
    from .class_point import Point

try:
    from class_sensor_handler import Sensor_handler
except ImportError:
    from .class_sensor_handler import Sensor_handler

try:
    from class_sensor import Sensor
except ImportError:
    from .class_sensor import Sensor



class Plotter():
    points = None
    lines = None
    sensors = None
    
    def __init__(self):
        self.lines = []
        self.points = set().copy()
        self.sensors = set().copy()
        self.sensor_handlers = set().copy()
# ============================================================================================================================================================
# for tests ==================================================================================================================================================
# ============================================================================================================================================================
        
# actual points of the room. Here hardcoded
# floor corners of my room
        Raumecke_nord_ost = Point("1",0,0,0)
        self.points = set([Raumecke_nord_ost])
        Raumecke_sued_ost = Point("2",3.9,0,0)
        self.points.add(Raumecke_sued_ost)
        Raumecke_sued_west = Point("3",3.9,5.4,0)
        self.points.add(Raumecke_sued_west)
        Raumecke_nord_west = Point("4",0,5.4,0)
        self.points.add(Raumecke_nord_west)
        
        # 1st level
        Schraege_nord_ost = Point("5",2.75,0,0.5)
        self.points.add(Schraege_nord_ost)
        Schraege_sued_ost = Point("6",3.9,0,0.5)
        self.points.add(Schraege_sued_ost)
        Schraege_sued_west = Point("7",3.9,5.4,0.5)
        self.points.add(Schraege_sued_west)
        Schraege_nord_west = Point("8",2.75,5.4,0.5)
        self.points.add(Schraege_nord_west)
        
        # 2nd level
        Decke_nord_ost = Point("9",0,0,2.3)
        self.points.add(Decke_nord_ost)
        Decke_nord_west = Point("10",0,5.4,2.3)
        self.points.add(Decke_nord_west)
        Decke_nord_ost_zu_dach = Point("11",0,2,2.3)
        self.points.add(Decke_nord_ost_zu_dach)
        Decke_nord_west_zu_dach = Point("12",0,3.4,2.3)
        self.points.add(Decke_nord_west_zu_dach)
        Decke_sued_ost_zu_dach = Point("13",3.9,2,2.3)
        self.points.add(Decke_sued_ost_zu_dach)
        Decke_sued_west_zu_dach = Point("14",3.9,3.4,2.3)
        self.points.add(Decke_sued_west_zu_dach)
        
        # 3rd level
        Dach_nord = Point("15",0,2.7,3.15)
        self.points.add(Dach_nord)
        Dach_sued = Point("16",3.9,2.7,3.15)
        self.points.add(Dach_sued)
        
        # connections
        # floor to floor
        Raumecke_nord_ost.adjacent_points_add([Raumecke_sued_ost,Raumecke_nord_west])
        Raumecke_sued_ost.adjacent_points_add([Raumecke_nord_ost,Raumecke_sued_west])
        Raumecke_sued_west.adjacent_points_add([Raumecke_nord_west,Raumecke_sued_ost])
        Raumecke_nord_west.adjacent_points_add([Raumecke_sued_west,Raumecke_nord_ost])
        
        # floor to 1st
        Raumecke_nord_ost.adjacent_points_add([])
        Raumecke_sued_ost.adjacent_points_add([Schraege_sued_ost])
        Raumecke_sued_west.adjacent_points_add([Schraege_sued_west])
        Raumecke_nord_west.adjacent_points_add([])
        
        # floor to 2nd
        Raumecke_nord_ost.adjacent_points_add([Decke_nord_ost])
        Raumecke_sued_ost.adjacent_points_add([])
        Raumecke_sued_west.adjacent_points_add([])
        Raumecke_nord_west.adjacent_points_add([Decke_nord_west])
        
        # 1st to 1st
        Schraege_nord_ost.adjacent_points_add([Schraege_sued_ost])
        Schraege_sued_ost.adjacent_points_add([Schraege_nord_ost])
        Schraege_sued_west.adjacent_points_add([Schraege_nord_west])
        Schraege_nord_west.adjacent_points_add([Schraege_sued_west])
        
        # 1st to 2nd & 3rd
        Schraege_nord_ost.adjacent_points_add([Decke_nord_ost,Decke_nord_ost_zu_dach])
        Schraege_sued_ost.adjacent_points_add([Decke_sued_ost_zu_dach])
        Schraege_sued_west.adjacent_points_add([Decke_sued_west_zu_dach])
        Schraege_nord_west.adjacent_points_add([Decke_nord_west,Decke_nord_west_zu_dach])
        
        # 2nd to 2nd
        Decke_nord_ost.adjacent_points_add([Decke_nord_ost_zu_dach])
        Decke_nord_west.adjacent_points_add([Decke_nord_west_zu_dach])
        Decke_nord_ost_zu_dach.adjacent_points_add([Decke_sued_ost_zu_dach,Decke_nord_ost, Decke_nord_west_zu_dach])
        Decke_nord_west_zu_dach.adjacent_points_add([Decke_sued_west_zu_dach,Decke_nord_west, Decke_nord_ost_zu_dach])
        Decke_sued_ost_zu_dach.adjacent_points_add([Decke_nord_ost_zu_dach,Decke_sued_west_zu_dach])
        Decke_sued_west_zu_dach.adjacent_points_add([Decke_nord_west_zu_dach,Decke_sued_ost_zu_dach])
        
        
        
        # 2nd to 3rd
        Decke_nord_ost.adjacent_points_add([])
        Decke_nord_west.adjacent_points_add([])
        Decke_nord_ost_zu_dach.adjacent_points_add([Dach_nord])
        Decke_nord_west_zu_dach.adjacent_points_add([Dach_nord])
        Decke_sued_ost_zu_dach.adjacent_points_add([Dach_sued])
        Decke_sued_west_zu_dach.adjacent_points_add([Dach_sued])
        
        # 3rd to 3rd
        Dach_nord.adjacent_points_add([Dach_sued])
        Dach_sued.adjacent_points_add([Dach_nord])
        
        
        
        # Sensor hardcodes
        esp8266_1 = Sensor(name = "esp8266_1",x=0.25,y=5.4-1.63,z=0.56)
        self.sensors.add(esp8266_1)
        handler_esp8266_1 = Sensor_handler(esp8266_1)
        self.sensor_handlers.add(handler_esp8266_1)
        esp8266_2 = Sensor(name = "esp8266_2",x=2.9,y=2.65,z=2.6)
        self.sensors.add(esp8266_2)
        handler_esp8266_2 = Sensor_handler(esp8266_2)
        self.sensor_handlers.add(handler_esp8266_2)
    
    def set_points(self,points):
        self.points = set(points)
    
    def plot_sensor_data(self, fig, ax, cb,normalize):
        data = []
        data_not_available = []
        for handler in self.sensor_handlers:
            coor = handler.sensor.return_coordinates_as_list().copy()
            val = handler.get_data_float()
            coor.append(val)
            if not(val == None):
                data.append(coor)
            else:
                data_not_available.append(coor)
        x = []
        y = []
        z = []
        v = []
        
        x_na = []
        y_na = []
        z_na = []
        for data_set in data:
            x.append(data_set[0])
            y.append(data_set[1])
            z.append(data_set[2])
            v.append(data_set[3])
        for data_set in data_not_available:
            x_na.append(data_set[0])
            y_na.append(data_set[1])
            z_na.append(data_set[2])
        s = ax.scatter(x,y,z, c=v, s=100, cmap=plt.get_cmap('viridis'), norm=normalize, alpha=1)
        s_na = ax.scatter(x_na,y_na,z_na, s=100, c='gray', alpha=0.3)
        return [cb, s, s_na, normalize]
    
    def plot_sensor_data_only(self, fig, ax, cb, s, s_na, normalize):
        data = []
        data_not_available = []
        
        for handler in self.sensor_handlers:
            coor = handler.sensor.return_coordinates_as_list().copy()
            val = handler.get_data_float()
            coor.append(val)
            if not(val == None):
                data.append(coor)
            else:
                data_not_available.append(coor)
        
        x = []
        y = []
        z = []
        v = []
        
        x_na = []
        y_na = []
        z_na = []
        
        for data_set in data:
            x.append(data_set[0])
            y.append(data_set[1])
            z.append(data_set[2])
            v.append(data_set[3])
        for data_set in data_not_available:
            x_na.append(data_set[0])
            y_na.append(data_set[1])
            z_na.append(data_set[2])
        s.remove()
        s_na.remove()
        s = ax.scatter(x,y,z, c=v, s=100, cmap=plt.get_cmap('viridis'),norm=normalize, alpha=1)
        s_na = ax.scatter(x_na,y_na,z_na, s=100, c='gray', alpha=0.3)
        plt.plot()
        return [ax, cb, s, s_na]
    
    def points_to_xyz(self):
        if(len(self.points) == 0):
            return False
        x_coor = []
        y_coor = []
        z_coor = []
        for item in self.points:
            x,y,z = item.return_coordinates()
            x_coor.append(x)
            y_coor.append(y)
            z_coor.append(z)
        return [x_coor, y_coor, z_coor]
    
    def get_neighbouring_pairs(self):
        if(len(self.points) == 0):
            return False
        neighbours = []
        for item in self.points: # iterates through the set of points
            for neighbour in item._set_proximity: # iterates through the saved ID-strings in the _set_proximity of item
                for target_point in self.points: # searches for the corresponding target_point to the neighbour-ID
                    if(target_point.ID == neighbour): # if that target-point is found, set the coordinates and break out of outer for loop
                        neighbours.append([item.return_coordinates(),
                                   target_point.return_coordinates()])
                        break
        return neighbours
    
    def draw_lines(self, fig, ax):
        if(len(self.points) == 0):
            return False
        
        point_pairs = self.get_neighbouring_pairs()
        for item in point_pairs:
            self.lines.append(ax.plot([item[0][0],item[1][0]],[item[0][1],item[1][1]],[item[0][2],item[1][2]],linestyle='--',color='blue',alpha=0.2))

    
    def plot_room(self, fig, ax, cb):
        if(len(self.points) == 0):
            return False
        x,y,z = self.points_to_xyz()
        if(ax!=None):
            ax.clear()
        if(ax==None):
            ax = fig.add_subplot(111,projection="3d")
        self.draw_lines(fig,ax)
        ax.set_xlabel("x-Axes")
        ax.set_ylabel("y-Axes")
        ax.set_zlabel("z-Axes")
        ax.set_xticks([0,1,2,3,4])
        ax.set_yticks([0,1,2,3,4,5,6])
        ax.set_zticks([0,1,2,3])
        normalize = Normalize(vmin=17, vmax=24)
        cb = fig.colorbar(mappable=ScalarMappable(norm=normalize, cmap=plt.get_cmap('viridis')),ax=ax, pad=0.1)
        cb.ax.set_xlabel("°C")
        
        return [ax,cb,normalize]
        
    def plot(self, fig, ax, cb, normalize):
        cb,s,s_na,normalize = self.plot_sensor_data(fig,ax,cb,normalize)

        return [ax,cb,s,s_na,normalize]
    
