##########################################################
##CENTRO DE ENSEÑANZA TÉCNICA Y SUPERIOR            ######
##Ingeniería en Cibernética Electrónica             ######
##Fernando Raúl Cortez Chávez                       ######
##28/10/17                                          ######
##Sistemas Operativos                               ######
###### Assignment 9: Weather Threading Locks    ##########

import json
import threading
import time
import urllib.request

# Global dictionary that will store the forecasts from all weather threads
weathers = {}
    
# Class that inherits from the Thread class
# Uses the OpenWeatherAPI with its "city" parameter to get a weather forecast
# After fetching the data, it stores it in the initialized global "weathers" list in the index
# equal to its threadID. Afterwards, it stays idle for "delay" seconds
class WeatherThread (threading.Thread):
    def __init__(self, city, delay):
        threading.Thread.__init__(self)
        self.city = city
        self.delay = delay
        self.lock = threading.Lock()

    def run(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'.format(self.city, "ea4dd97a55fefeb38dcd3364cbacfd74")
        with urllib.request.urlopen(url) as r:
            # Lock the network access code line
            self.lock.acquire()

            # Obtain a response from the Open Weather API
            response = r.read()

            # Release the lock
            self.lock.release()

            # Parse the response
            encoding = r.info().get_content_charset('utf-8')
            data = json.loads(response.decode(encoding))
            weather_info = {"city":self.city, "max":data["main"]["temp_max"], "min":data["main"]["temp_min"], "description":data["weather"][0]["description"]}
            weathers[self.city] = weather_info
            time.sleep(self.delay)
               
def start_program():
    # Start taking the time needed to finish fetching the weather data
    start = time.time()

    # List with all cities to be passed as parameters to the WeatherThread class
    ciudades = ["Tijuana", "Mexicali", "Ensenada", "Rosarito", "Tecate", "La%20Paz", "Loreto", "Mulege", "Hermosillo", "Aguascalientes", "Queretaro", "Monterrey", "Guadalajara", "Culiacan", "Morelia", "Mazatlan", "Tepic", "Mazatlan", "Tequila", "Guamuchil", "Tijuana", "Mexicali", "Ensenada", "Rosarito", "Tecate", "La%20Paz", "Loreto", "Mulege", "Hermosillo", "Aguascalientes", "Queretaro", "Monterrey", "Guadalajara", "Culiacan", "Morelia", "Mazatlan", "Tepic", "Mazatlan", "Tequila", "Guamuchil"]

    # Declare a list that will contain references to all threads created
    threadsList = []

    # Introductory string 
    print("Vamos a buscar el clima de {0} ciudades".format(len(ciudades)))
    
    # Create instances of the WeatherThread class
    for ciudad in ciudades:
        weathers[ciudad] = ""
        thread = WeatherThread(ciudad, 2)
        thread.setDaemon(True)
        thread.start()
        threadsList.append(thread)

    # Wait for all threads to finish
    for thread_weather in threadsList:
        thread_weather.join()

    # Obtain the period of time used to get the weather forecasts
    end = time.time()
    print("Obtener los pronósticos tardó {0} segundos\n".format(end - start))

    # Print the forecasts in order
    for info in list(weathers.values()):
        city = info["city"]
        temperatura_maxima = info["max"] - 273.15
        temperatura_minima = info["min"] - 273.15
        extra_info = info["description"]

        print("La temperatura máxima para la ciudad de {0} es de {1:.0f}".format(city, temperatura_maxima))
        print("\t con una temperatura mínima de {0:.2f} y clima {1}\n".format(temperatura_maxima, extra_info))

# Start the main function
start_program()
