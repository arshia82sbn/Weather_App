import os
from datetime import datetime
from os.path import dirname
import pytz
import requests
from CTkMessagebox import CTkMessagebox
from PIL import Image,ImageTk
from customtkinter import *
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import threading

# Initial application setup and GUI configuration
root = CTk()  # Create main window using customtkinter
root.geometry("800x500+300+200")  # Set window size and position
root.title("Weather App")  # Set window title
root.config(bg="#E3F3FD")  # Set background color
root.resizable(False, False)  # Disable window resizing
# Logo icon
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
logo_icon = ImageTk.PhotoImage(Image.open(logo_path))
root.iconphoto(False, logo_icon)
root.after(250, lambda: root.iconphoto(False, logo_icon))
# Weather icons
nots = ["WIND", "HUMIDITY", "DESCRIPTION", "PRESSURE"]
base_address = os.path.dirname(__file__)  # Base path of executable file
icons_paths = [
    os.path.join(base_address, "wind.png"),
    os.path.join(base_address, "humidity.png"),
    os.path.join(base_address, "description.png"),
    os.path.join(base_address, "pressure.png")
]


# Function to get geographical information of a city
def get_location(city):
    """Get geographical coordinates of a city using geopy.

    Args:
        city (str): City name entered by user

    Returns:
        Location object or None: Location information or None on error
    """
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if location:
            return location
        CTkMessagebox(title="Error", message="City not found!", icon="cancel")
        return None
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Location error: {e}", icon="cancel")
        return None


# Function to get timezone
def get_timezone(location):
    """Get timezone based on geographical coordinates.

    Args:
        location (Location): Geographical location object

    Returns:
        pytz.timezone or None: Timezone or None on error
    """
    try:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        return pytz.timezone(timezone_str)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Timezone error: {e}", icon="cancel")
        return None


# Function to get weather data from API
def get_weather_data(city):
    """Get weather information from OpenWeatherMap API.

    Args:
        city (str): City name

    Returns:
        dict or None: JSON data or None on error
    """
    api_key = "Your API Key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        json_data = response.json()
        if json_data["cod"] != 200:
            CTkMessagebox(title="Error", message=f"API Error: {json_data['message']}", icon="cancel")
            return None
        return json_data
    except requests.exceptions.ConnectionError:
        CTkMessagebox(title="Error", message="Connection error: Check your network.", icon="cancel")
        return None
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Weather data error: {e}", icon="cancel")
        return None


# Main function to update weather information
def getWeather():
    """Get and display weather information based on user input."""
    city = entry.get().strip()
    if not city:
        CTkMessagebox(title="Warning", message="Please enter a city name!", icon="warning")
        return

    # Get location information
    location = get_location(city)
    if not location:
        return

    # Get timezone
    timezone = get_timezone(location)
    if not timezone:
        return

    # Calculate and display local time
    local_time = datetime.now(timezone)
    current_time = local_time.strftime("%H:%M:%S \n%Y/%m/%d")
    clock.configure(text=current_time)
    name.configure(text=f"Your city: {city}")

    # Get and process weather data
    json_data = get_weather_data(city)
    if not json_data:
        return

    condition = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = round(json_data['main']['temp'] - 273.15, 1)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    # Update UI labels
    t.configure(text=f"{temp}°C")
    c.configure(text=f"{condition} | FEELS LIKE {temp}°C")
    w.configure(text=f"{wind} m/s")
    h.configure(text=f"{humidity}%")
    d.configure(text=description.capitalize())
    p.configure(text=f"{pressure} hPa")


# GUI - User input
entry = CTkEntry(root, bg_color="#E3F3FD", fg_color="#E3F3FD", width=520, height=50, text_color="#404040")
entry.place(x=270, y=17)

# Load and display logo
logo_image = Image.open(os.path.join(base_address, "weather-app.png"))
logo_image = logo_image.resize((200, 200))
logo_photo = CTkImage(logo_image,size=(120,120))
logo = CTkLabel(root, image=logo_photo, text="", bg_color="#E3F3FD")
logo.place(x=250, y=150)

# Search button with icon
search_icon = CTkImage(Image.open(os.path.join(base_address, "search_icon.png")),size=(30,30))
search_button = CTkButton(
    root,
    image=search_icon,
    text="",
    border_width=0,
    cursor="hand2",
    fg_color="#E3F3FD",
    bg_color="#E3F3FD",
    width=40,
    command=lambda: threading.Thread(target=getWeather).start(),
    hover_color="#E3F3FD"
)
search_button.place(x=740, y=23)

# Background frame for weather information
frame = CTkFrame(root, width=750, height=100, corner_radius=20, fg_color="#1ab5ef", bg_color="#E3F3FD")
frame.place(x=40, y=380)

# Display time and city name
name = CTkLabel(root, font=('Arial', 15, 'bold'), text_color="#404040", bg_color="#E3F3FD")
name.place(x=30, y=100)
clock = CTkLabel(root, font=('Helvetica', 20), text_color="#404040", bg_color="#E3F3FD")
clock.place(x=30, y=130)

# Weather information display labels
t = CTkLabel(root, font=('Arial', 70, 'bold'), text_color="#ee666d", bg_color="#E3F3FD")
t.place(x=400, y=150)
c = CTkLabel(root, font=('Arial', 15, 'bold'), text_color="#000000", bg_color="#E3F3FD")
c.place(x=400, y=250)

# Load icons and labels for weather information
weather_labels = []
for i, (note, icon_path) in enumerate(zip(nots, icons_paths)):
    icon_image = Image.open(icon_path).resize((40, 40), Image.LANCZOS)
    icon_photo = CTkImage((icon_image))
    label = CTkLabel(
        root,
        text=note,
        image=icon_photo,
        compound="left",
        font=("Helvetica", 15, 'bold'),
        text_color="#ffffff",
        bg_color="#1ab5ef",
        padx=5,
        pady=5
    )
    label.place(x=60 + i * 200, y=390)
    weather_labels.append(label)

# Placeholder labels for weather details
w = CTkLabel(root, text="1", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
w.place(x=80, y=430)
h = CTkLabel(root, text=" ", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
h.place(x=300, y=430)
d = CTkLabel(root, text=" ", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
d.place(x=500, y=430)
p = CTkLabel(root, text=" ", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
p.place(x=700, y=430)

# Run main application loop
root.mainloop()