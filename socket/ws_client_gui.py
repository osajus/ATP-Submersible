import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import tkinterweb

#https://coderslegacy.com/figurecanvastkagg-matplotlib-tkinter/

con = sqlite3.connect("rov_local.db")
cur = con.cursor()

root = tk.Tk()
root.title("ROV Client")
root.geometry("1000x900")

f = plt.Figure(figsize=(5,7), dpi=90)
chamber_subplt = f.add_subplot(221) # rows, cols, # of this subplot
water_subplt = f.add_subplot(222)
pressurePSI_subplt = f.add_subplot(223)
pressureFT_subplt = f.add_subplot(224)


def get_chamber_temps(interval):
    chamber_temps = {}
    for row in cur.execute('SELECT dataID, chamber_tempF from data'):
        chamber_temps[row[0]] = row[1]
    chamber_subplt.clear()
    chamber_subplt.set_title("Chamber 'F")
    f.tight_layout()
    chamber_subplt.plot(chamber_temps.keys(), chamber_temps.values())

def get_water_temps(interval):
    water_temps = {}
    for row in cur.execute('SELECT dataID, sensor_tempF from data'):
        water_temps[row[0]] = row[1]
    water_subplt.clear()
    water_subplt.set_title("Water 'F")
    water_subplt.plot(water_temps.keys(), water_temps.values())

def get_pressure_psi(interval):
    pressurePSI = {}
    for row in cur.execute('SELECT dataID, pressure_psi from data'):
        pressurePSI[row[0]] = row[1]
    pressurePSI_subplt.clear()
    pressurePSI_subplt.set_title("Pressure PSI")
    pressurePSI_subplt.plot(pressurePSI.keys(), pressurePSI.values())
    
def get_pressure_ft(interval):
    pressureFT = {}
    for row in cur.execute('SELECT dataID, pressure_ft from data'):
        pressureFT[row[0]] = row[1]
    pressureFT_subplt.clear()
    pressureFT_subplt.set_title("Pressure FT")
    pressureFT_subplt.plot(pressureFT.keys(), pressureFT.values())

    


frame1 = tk.LabelFrame(root, text="charts", padx=10, pady=10)
frame1.pack(padx=15, pady=15)

frame2 = tkinterweb.HtmlFrame(root)
frame2.load_website("http://rov:8080/stream/snapshot.jpeg?delay_s=0")
frame2.pack()


canvas = FigureCanvasTkAgg(f, root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
ani1 = animation.FuncAnimation(f, get_chamber_temps, 1000)
ani2 = animation.FuncAnimation(f, get_water_temps, 1000)
ani3 = animation.FuncAnimation(f, get_pressure_psi, 1000)
ani4 = animation.FuncAnimation(f, get_pressure_ft, 1000)


root.mainloop()
