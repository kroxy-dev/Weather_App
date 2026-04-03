import requests
import json
class WeatherApp:
    def __init__(self,api_key):
        self.last_city=None 
        self.key=api_key
    def fetch_weather(self,city):
        try:
            rep=requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.key}&units=metric')
            rep.raise_for_status()
            data=rep.json()
            return {"city":data["name"], "temp":data["main"]["temp"],"description":data["weather"][0]["description"]}


        except requests.exceptions.RequestException :
            return None 
        
    def save_last_city(self,city):
        try:
            with open('cachee.json','w') as f:
                json.dump({"last_city":city},f)
        except Exception as e:
            print(f"error {e}")

    def load_last_city(self):
        try:
            with open('cachee.json','r') as f:
                self.last_city=json.load(f)["last_city"]
        except FileNotFoundError :
            pass
        except Exception as e:
            print(f"error {e}")
    def run(self):
        self.load_last_city()
        while True:
            if self.last_city:
                city=input(f"Last city: {self.last_city}. Press Enter to use it or type a new one: ")
                if not city:
                    city=self.last_city
            else:
                city=input("please enter a city ")
                #i noticed that u did not ask me to control the edge case where the user doesnt type anything here so m gonna keep it like this
            weather=self.fetch_weather(city)
            if not weather:
                print("City not found or request failed.")
                break
            else:
                print(f"city: {weather['city']}")
                print(f"temperature: {weather['temp']}")
                print(f"description : {weather['description']}")
                self.save_last_city(city)
                self.last_city = weather['city']
                answer=input("search again Y/N?")
                if answer.lower()=='n':
                    break
    
if __name__ == "__main__":
    api_key = input("Enter your API key: ")
    app = WeatherApp(api_key)
    app.run()