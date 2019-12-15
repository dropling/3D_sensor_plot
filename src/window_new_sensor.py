import tkinter as tk
from class_sensor import Sensor


class New_sensor_window(tk.Toplevel):
    def __init__(self, parent, title='New Sensor'):
        
        tk.Toplevel.__init__(self, parent)
        
        if title:
            self.title(title)
            
        self.parent = parent
        
        self.create_widgets()
        
    def create_widgets(self):
        self.sensor_name_label = tk.Label(self, text="Sensor name")
        self.sensor_name_label.pack()
        self.sensor_name_entry = tk.Entry(self)
        self.sensor_name_entry.pack()
        
        self.sensor_position_x_label = tk.Label(self, text="X-Position")
        self.sensor_position_x_label.pack()
        self.sensor_position_x_entry = tk.Entry(self)
        self.sensor_position_x_entry.pack()
        
        self.sensor_position_y_label = tk.Label(self, text="Y-Position")
        self.sensor_position_y_label.pack()
        self.sensor_position_y_entry = tk.Entry(self)
        self.sensor_position_y_entry.pack()
        
        self.sensor_position_z_label = tk.Label(self, text="Z-Position")
        self.sensor_position_z_label.pack()
        self.sensor_position_z_entry = tk.Entry(self)
        self.sensor_position_z_entry.pack()
        
        self.sensor_callibration_label = tk.Label(self, text="Callibration constant")
        self.sensor_callibration_label.pack()
        self.sensor_callibration_entry = tk.Entry(self)
        self.sensor_callibration_entry.pack()
        
        self.button = tk.Button(self, text="Save and close", command=lambda: self.save_and_destroy())
        self.button.pack()
        
    def save_and_destroy(self):
        name = self.sensor_name_entry.get()
        x = self.sensor_position_x_entry.get()
        y = self.sensor_position_y_entry.get()
        z = self.sensor_position_z_entry.get()
        callibration = self.sensor_callibration_entry.get()
        sensor = None
        if name and x and y and z:
            if callibration:
                sensor = Sensor(name = name, x = x, y = y, z = z, cal_constant = callibration)
            sensor = Sensor(name = name, x = x, y = y, z = z)
            print(sensor)
            self.parent.plotter.add_sensor(sensor)
            print(self.parent.plotter.sensors)
            self.parent.plotter.initialize_sensor_handlers()
        self.destroy()