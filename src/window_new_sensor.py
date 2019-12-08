import tkinter as tk



class New_sensor_window(tk.Toplevel):
    def __init__(self, parent, title='New Sensor'):
        
        tk.Toplevel.__init__(self, parent)
        
        if title:
            self.title(title)
            
        self.parent = parent
        
        self.create_widgets()
        
    def create_widgets(self):
        sensor_name_label = tk.Label(self, text="Sensor name")
        sensor_name_label.pack()
        sensor_name_entry = tk.Entry(self)
        sensor_name_entry.pack()
        
        sensor_position_x_label = tk.Label(self, text="X-Position")
        sensor_position_x_label.pack()
        sensor_position_x_entry = tk.Entry(self)
        sensor_position_x_entry.pack()
        
        sensor_position_y_label = tk.Label(self, text="Y-Position")
        sensor_position_y_label.pack()
        sensor_position_y_entry = tk.Entry(self)
        sensor_position_y_entry.pack()
        
        sensor_position_z_label = tk.Label(self, text="Z-Position")
        sensor_position_z_label.pack()
        sensor_position_z_entry = tk.Entry(self)
        sensor_position_z_entry.pack()
        
        sensor_callibration_label = tk.Label(self, text="Callibration constant")
        sensor_callibration_label.pack()
        sensor_callibration_entry = tk.Entry(self)
        sensor_callibration_entry.pack()
        
        button = tk.Button(self, text="Save and close", command=lambda: self.save_and_destroy())
        button.pack()
        
    def save_and_destroy(window):
        window.destroy()