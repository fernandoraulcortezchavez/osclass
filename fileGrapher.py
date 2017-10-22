import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time
from hurry.filesize import size
import threading
import os

PATH = "/"

fileCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0}
formatMemoryCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0} 
textExtensions = [".txt", ".pdf"]
audioExtensions = [".mp3", ".mid", ".midi", ".wav", ".wmv", ".cda", ".ogg", ".ogm", ".aac", ".ac3", ".flac"]
videoExtensions = [".avi", ".flv", ".wmv", ".mov", ".mp4"]
photoExtensions = [".bmp", ".gif", ".jpg", ".png", ".psd", ".ai", ".svg", ".raw"]

def searchFileType(fileType, extensions = None):
    for root, dirs, files in os.walk(PATH):
        for name in files:
            #if name.endswith(".py"):
            #    txtFiles += 1
            newPath = os.path.join(root, name)
            if os.path.exists(newPath):
                if fileType == "apps" and ("." not in name):
                    fileCounter["apps"] += os.stat(newPath).st_size
                elif fileType == "all":
                    fileCounter["all"] += os.stat(newPath).st_size
                elif extensions is not None and any(name.endswith(x) for x in extensions):
                    fileCounter[fileType] += os.stat(newPath).st_size

def classifyFiles():
    #initialize dictionaries
    global fileCounter, formatMemoryCounter
    fileCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0}
    formatMemoryCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0}


    threadTxt = threading.Thread(target = searchFileType, args = ("text", textExtensions,))
    threadApp = threading.Thread(target = searchFileType, args = ("apps", ))
    threadAudio = threading.Thread(target = searchFileType, args = ("audios", audioExtensions,))
    threadVideo = threading.Thread(target = searchFileType, args = ("videos", videoExtensions,))
    threadPhoto = threading.Thread(target = searchFileType, args = ("photos", photoExtensions,))
    threadAll = threading.Thread(target = searchFileType, args = ("all", ))

    threads = []
    threads.append(threadTxt)
    threads.append(threadApp)
    threads.append(threadAudio)
    threads.append(threadVideo)
    threads.append(threadPhoto)
    threads.append(threadAll)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    fileCounter["other"] = fileCounter["all"] - sum((list(fileCounter.values()))[1:-1])
    for key in list(fileCounter.keys()):
        formatMemoryCounter[key] = size(fileCounter[key])

ax = None
labels = []
mem = []
values = []

def appendLabelValues():
    newList = []
    for i in range(len(labels)):
        newList.append(labels[i] + " " + str(mem[i]))
    return newList

def convertToPercents(numbersList):
    total = sum(numbersList)
    for num in numbersList:
        num = (num * 100) / total
    return numbersList

def updateGraph(event):
    global labels, mem, values

    classifyFiles()
    labels = (list(formatMemoryCounter.keys()))[1:]
    mem = (list(formatMemoryCounter.values()))[1:]
    values = convertToPercents((list(fileCounter.values()))[1:])

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

classifyFiles()
labels = (list(formatMemoryCounter.keys()))[1:]
mem = (list(formatMemoryCounter.values()))[1:]
values = convertToPercents((list(fileCounter.values()))[1:])

initializeGraph()
