import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

ax = None
labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
mem = ["1GB", "2GB", "0.5GB", "4MB"]
values = [20, 20, 20, 40]

def appendLabelValues():
    newList = []
    for i in range(len(labels)):
        newList.append(labels[i] + " " + mem[i])
    return newList

def updateGraph(event):
    global values
    values = [15, 0.5, 14.5, 70]

    l = appendLabelValues()
    # Erase previous version of the graph
    ax.clear()

    # Draw a new graph
    p = ax.pie(values, autopct='%1.1f%%')
    ax.axis('equal')

    # Update legend
    ax.legend(p[0], l, loc = "center left")

    # Show again the graph
    plt.draw()
    print("I was clicked")

def initializeGraph():
    global ax

    l = appendLabelValues()
    # Set up graph
    fig, ax = plt.subplots()
    p = ax.pie(values, autopct='%1.1f%%')
    ax.axis('equal')

    # Set up legend
    ax.legend(p[0], l, loc="lower left")

    # Set up Refresh buton
    axRefresh = plt.axes([0.81, 0.05, 0.1, 0.075])
    btnRefresh = Button(axRefresh, "Refresh")
    btnRefresh.on_clicked(updateGraph)

    # Show the graph for the first time
    plt.show()

#initializeGraph()
