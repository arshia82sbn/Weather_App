# ☀️ Weather App with Python

Welcome to my weather app! This is a simple and attractive application built with Python that displays the weather information of any city you like. It uses the **OpenWeatherMap API** to fetch data and has a UI built with **customtkinter** which is both sleek and user-friendly! 🌍

##
![Weather App Screenshot](screenshot.png)
##

## ✨ Features

This app has some cool features that make using it enjoyable:

- 🌡️ **Display Weather Information**: View temperature (in Celsius), humidity, wind speed, and air pressure.
- ⏰ **Local City Time**: Shows the local time and date of the city based on its exact timezone.
- 🎨 **Beautiful UI**: Minimal and attractive design with pleasant colors and cute icons.
- 🚨 **Error Handling**: If something is wrong (like the city name or internet), a clear and user-friendly error message is shown.

---

## 🛠️ Installation & Setup

To run the app, just follow these simple steps:

1. **Install Python** 🐍\
   If you haven't installed Python, download and install version 3.x from the [official Python website](https://www.python.org/downloads/).

2. **Install Required Libraries** 📚\
   Run this command in your terminal or command prompt to install dependencies:

   ```bash
   pip install customtkinter requests geopy timezonefinder pillow CTkMessagebox
   ```

3. **Get API Key from OpenWeatherMap** 🔑

   - Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account.
   - After signing up, you'll receive an **API Key**. Add it to the `api_key` variable inside the `get_weather_data` function:
     ```python
     api_key = "Your API Key"  # Replace this with your own key!
     ```

4. **Run the App** 🚀\
   Use this command to run the program:

   ```bash
   python weather_app.py
   ```

> **Note**: Make sure icon files (`logo.png`, `wind.png`, `humidity.png`, `description.png`, `pressure.png`, `search_icon.png`, `weather-app.png`) are in the same folder as `weather_app.py`!

---

## 📖 How to Use

Using the app is super easy:

1. Open the app.
2. Enter the name of the city in the input field (e.g., `Tehran` or `London`).
3. Click the search button (🔍).
4. View the weather info, local time, and other details!

If something goes wrong (e.g., wrong city name or no internet), an error message will be shown.

---

## 🌐 About the API

This app uses the [**OpenWeatherMap API**](https://openweathermap.org/api), one of the best and most popular weather data services. It provides accurate and up-to-date data from around the world. To use it:

- Register on their website (it's free!).
- Get a free API key and paste it into your code.
- Requests are sent like this:
  ```
  https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}
  ```

The data is returned in JSON format, and our app converts the temperature from Kelvin to Celsius to make it easier to read!

---

## 🧰 Code Structure

The code is written in a modular format, and the main functions are:

- `` 📍\
  Finds the geographic coordinates (latitude & longitude) of a city using **geopy**.

- `` ⏳\
  Calculates the timezone of the city using **timezonefinder** to accurately display the local time.

- `` 🌦️\
  Fetches weather information (temperature, humidity, wind, etc.) from the API and reports any errors.

- `` 🚀\
  The main function that ties everything together: gets user input, processes data, and updates the UI.

The UI is built using **customtkinter** which manages widgets like buttons, entries, and labels in a stylish way.

---

## 📦 Dependencies

The app depends on the following libraries:

- **Python 3.x** 🐍
- **customtkinter** 🎨 – For the stylish graphical interface
- **requests** 🌐 – To make API calls
- **geopy** 📍 – To find city coordinates
- **timezonefinder** ⏰ – To calculate the timezone
- **Pillow** 🖼️ – To load and manage images
- **CTkMessagebox** 🚨 – For showing error/warning messages

Install them with this simple command:

```bash
pip install customtkinter requests geopy timezonefinder pillow CTkMessagebox
```

---

## 🖼️ Icons & Assets

The app uses several nice icons that should be in the project folder:

- `logo.png` – App logo
- `wind.png` – Wind speed icon
- `humidity.png` – Humidity icon
- `description.png` – Weather description icon
- `pressure.png` – Air pressure icon
- `search_icon.png` – Search button icon
- `weather-app.png` – Main app image

If you don't have these files, you can download similar ones from sites like [Flaticon](https://www.flaticon.com/).

---

## 📬 Contact Me

If you have questions, suggestions, or want to collaborate, I’d love to hear from you:

- **Email**: [Arshia82sbn@gmail.com](mailto\:Arshia82sbn@gmail.com)

---

Hope you enjoy this app! If you have any ideas for improvements, feel free to reach out. 🌟

