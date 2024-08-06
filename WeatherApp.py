import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

API_KEY = 'dde51638bc7c5c93dbe98122389116d0'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather_data(location):
    try:
        response = requests.get(BASE_URL, params={'q': location, 'appid': API_KEY, 'units': 'metric'})
        data = response.json()
        if data['cod'] == 200:
            return data
        else:
            messagebox.showerror("Error", "Location not found.")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def update_weather():
    location = location_entry.get()
    data = get_weather_data(location)
    if data:
        city = data['name']
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))

        city_label.config(text=f"City: {city}")
        temp_label.config(text=f"Temperature: {temp}°C")
        weather_label.config(text=f"Weather: {weather.capitalize()}")
        weather_icon = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon

# Create GUI
window = tk.Tk()
window.title("Weather App")

tk.Label(window, text="Enter Location:").grid(row=0, column=0)
location_entry = tk.Entry(window)
location_entry.grid(row=0, column=1)

search_button = tk.Button(window, text="Get Weather", command=update_weather)
search_button.grid(row=1, column=0, columnspan=2)

city_label = tk.Label(window, text="")
city_label.grid(row=2, column=0, columnspan=2)

temp_label = tk.Label(window, text="")
temp_label.grid(row=3, column=0, columnspan=2)

weather_label = tk.Label(window, text="")
weather_label.grid(row=4, column=0, columnspan=2)

icon_label = tk.Label(window)
icon_label.grid(row=5, column=0, columnspan=2)

window.mainloop()
