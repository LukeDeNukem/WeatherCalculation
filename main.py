import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget): 
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter your desired place: ", self) 
        self.city_input = QLineEdit(self) #textbox 
        self.get_answer = QPushButton("Calculate", self) #declared button for calculating the weather in desired place.
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc_label = QLabel(self) #last two declarations are for the result itself.
        self.initUI()

    def initUI(self): #defining a UI for better and more practical use of the app.


        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_answer)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.desc_label)
        vbox.addWidget(self.emoji_label)

        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter) #These lines of code are used for aligning the objects we have in our app.
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label") #These lines of code are used for declaring the object names for styling.
        self.city_input.setObjectName("city_input")
        self.get_answer.setObjectName("get_answer")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.desc_label.setObjectName("desc_label")

        #This piece of code is used for basic styling of the whole application.    
        self.setStyleSheet(""" 
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: bold;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_answer{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#desc_label{
                font-size: 50px;
            }
        """)

        self.get_answer.clicked.connect(self.get_weather) #This triggers the get_weather line of code once the calculate button is clicked.
    
    def get_weather(self): #This block of code helps me get the right data.

        api_key = "2184ce7296d0acd0d4643154f105f8f6"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:  
           response = requests.get(url)
           response.raise_for_status()
           data = response.json()

           if data["cod"] == 200:
              self.display_weather(data)
        except requests.exceptions.HTTPError: #This block of code is used for defining the type of errors an individual can stumble upon whilst calculating the weather.
           match response.status_code:
               case 400:
                    self.display_error("Bad Request\nPlease check your input!")
               case 401:
                    self.display_error("Unauthorized\nInvalid API key!")
               case 403:
                    self.display_error("Forbidden\nAccess is denied!")
               case 404:
                    self.display_error("Not Found\nCity not found!")
               case 500:
                    self.display_error("Internal Server Error\nTry again later!")
               case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
               case 503:
                    self.display_error("Service Unavailable\nServer is down")
               case 504:
                    self.display_error("Gateway Timeout\nNo response from the server!")
               case _:
                    self.display_error("HTTP Error occured\n{http_error}")
           
        except requests.RequestException:
            pass
        
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data): #This block of code calculates the temperature from kalvin to celsius and fahrenheit and displays the two units without the decimals.
        self.temperature_label.setStyleSheet("font-size: 30px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = 9/5 * temperature_c + 32
        self.temperature_label.setText(f"Temperature in Celsius: {temperature_c:.0f} \n Temperature in Fahrenheit: {temperature_f:.0f}")

if __name__ == "__main__":
    app = QApplication(sys.argv) #This is not gonna be used because we're not gonna send any arguments to our system. I put it here for convenience sake, it was a tip from Internet wizards.
    weather_app = WeatherApp() 
    weather_app.show() #Commands the program to show the previously mentioned widget. 
    sys.exit(app.exec_()) #Allows the app to stay open and let's us close it, maximize-minimize...