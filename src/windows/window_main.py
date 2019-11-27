import tkinter as tk
from matplotlib.figure import Figure
import time

try:
    import data_and_plotting.plot_main as mplot
except ImportError:
    import windows.data_and_plotting.plot_main as mplot


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

try:
    from window_new_sensor import New_sensor_window
except ImportError:
    from .window_new_sensor import New_sensor_window


class Main_window(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self)
        self.bool_plot = True
        self.create_widgets()
        self.bind("<<event_refresh_canvas>>", self.refresh_canvas)
        
    def create_widgets(self):
        # create a menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        self.geometry("640x450")
        
        # Menu items
        # File menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=lambda: self.callback())
        filemenu.add_command(label="Open File", command=lambda: self.callback())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=lambda: self.exit())
        # Sensor menu
        sensormenu = tk.Menu(menu)
        menu.add_cascade(label="Sensors", menu=sensormenu)
        sensormenu.add_command(label="New Sensor", command=lambda: self.window_open_new_sensor())
        sensormenu.add_command(label="Delete Sensor", command=lambda: self.callback())
        # Help menu
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=lambda: self.callback())
        
        # Canvas for plots
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
    def refresh_canvas(self, *args):
        self.canvas.draw()
        
    def thread_plot_procedures(self):
        time.sleep(1)
        
        self.ax = None
        self.cb = None
        self.sensor_scatter = None
        self.sensor_scatter_na = None
        self.normalize = None
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.ax, self.cb, self.normalize = mplot.plot_room(self.fig,self.ax,self.cb)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.update()
        self.event_generate("<<event_refresh_canvas>>")
        self.ax, self.cb, self.sensor_scatter, self.sensor_scatter_na, self.normalize = mplot.plot(self.fig,self.ax,self.cb,self.normalize)
        
        while(self.bool_plot):
            self.ax, self.cb, self.sensor_scatter, self.sensor_scatter_na = mplot.plot_sensor_data_only(self.fig, self.ax, self.cb, self.sensor_scatter, self.sensor_scatter_na, self.normalize)
            self.event_generate("<<event_refresh_canvas>>")
        
        # Callback functions
    def window_open_new_sensor(self):
        window = New_sensor_window(self)
        return
        
    def callback(self):
        print("called the callback!")
        return

    def exit(self):
        self.bool_plot = False
        time.sleep(2)
        self.save_state()
        self.destroy()
        
    def save_state(self):
        pass