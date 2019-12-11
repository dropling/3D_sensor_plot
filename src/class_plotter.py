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

try:
    from class_file_manager import File_manager
except ImportError:
    from .class_file_manager import File_manager


class Plotter():
    points = None
    lines = None
    sensors = None
    file_manager = None # not implemented just yet
    
    def __init__(self):
        self.lines = []
        self.points = set().copy()
        self.sensors = set().copy()
        self.sensor_handlers = set().copy()
# ============================================================================================================================================================
# for tests ==================================================================================================================================================
# ============================================================================================================================================================

        self.load_points('test_points.json')
        self.load_sensors('test_sensors.json')
        self.initialize_sensor_handlers()

    def set_points(self,points):
        self.points = set(points)
        return True
    
    def load_points(self, file_name):
        file_manager = File_manager(mode = 'r')
        file_manager.set_file(file_name)
        if(file_manager.load_data()):
            self.points = set(file_manager.return_points_list())
        
    
    def save_points(self, file_name):
        file_manager = File_manager(mode = 'w')
        file_manager.set_file(file_name)
        file_manager.save_points(self.points)
        
    def load_sensors(self, file_name):
        file_manager = File_manager(mode = 'r')
        file_manager.set_file(file_name)
        if(file_manager.load_data()):
            self.sensors = set(file_manager.return_sensors_list())
    
    def save_sensors(self, file_name):
        file_manager = File_manager(mode = 'w')
        file_manager.set_file(file_name)
        file_manager.save_sensors(self.sensors)
        
    def initialize_sensor_handlers(self):
        self.sensor_handlers = set().copy()
        for sensor in self.sensors:
            self.sensor_handlers.add(Sensor_handler(sensor))
    
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
    
