import tkinter as tk
import threading

from window_main import Main_window

if __name__ == '__main__':
    root = Main_window()
    
    
    # Multithread over here for the sensor-data
    figure_refresher = threading.Thread(target=root.thread_plot_procedures)
    figure_refresher.start()
    tk.mainloop()