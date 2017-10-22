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

texts = []
apps = []
audios = []
videos = []
photos = []
other = []

def searchFileType():
    global texts, apps, audios, videos, photos, other
    texts, apps, audios, videos, photos, other = [], [], [], [], [], []

    for root, dirs, files in os.walk(PATH):
        for name in files:
            #if name.endswith(".py"):
            #    txtFiles += 1
            newPath = os.path.join(root, name)
            if os.path.exists(newPath) and os.path.isfile(newPath):
                mem = os.path.getsize(newPath)
                p, ext = os.path.splitext(newPath)
                if "." not in name or os.access(newPath, os.X_OK):
                    apps.append(mem)
                elif ext in textExtensions:
                    texts.append(mem)
                elif ext in audioExtensions:
                    audios.append(mem)
                elif ext in videoExtensions:
                    videos.append(mem)
                elif ext in photoExtensions:
                    photos.append(mem)
                else:
                    other.append(mem)
   
def calculate(ext):
    total = 0
    if ext == "text":
        total = sum(texts)
    elif ext == "apps":
        total = sum(apps)
    elif ext == "audios":
        total = sum(audios)
    elif ext == "videos":
        total = sum(videos)
    elif ext == "photos":
        total = sum(photos)
    elif ext == "other":
        total = sum(other)
    fileCounter[ext] = total

def classifyFiles():
    #initialize dictionaries
    global fileCounter, formatMemoryCounter
    fileCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0}
    formatMemoryCounter = {"all":0, "text":0, "apps":0, "audios":0, "videos":0, "photos":0, "other":0}
    
    searchFileType()

    threadTxt = threading.Thread(target = calculate, args = ("text",))
    threadApp = threading.Thread(target = calculate, args = ("apps", ))
    threadAudio = threading.Thread(target = calculate, args = ("audios",))
    threadVideo = threading.Thread(target = calculate, args = ("videos",))
    threadPhoto = threading.Thread(target = calculate, args = ("photos",))
    threadOther = threading.Thread(target = calculate, args = ("other", ))

    threads = []
    threads.append(threadTxt)
    threads.append(threadApp)
    threads.append(threadAudio)
    threads.append(threadVideo)
    threads.append(threadPhoto)
    threads.append(threadOther)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    fileCounter["all"] = sum((list(fileCounter.values()))[1:])
    for key in list(fileCounter.keys()):
        formatMemoryCounter[key] = size(fileCounter[key])
    print(fileCounter)
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
