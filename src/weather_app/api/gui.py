import threading
from pathlib import Path

from CTkMessagebox import CTkMessagebox
from PIL import Image
from customtkinter import (
    CTk, CTkButton, CTkEntry, CTkFrame, CTkImage, CTkLabel
)

from weather_app.api.facade import WeatherFacade
from weather_app.models.weather import WeatherData

ASSETS_DIR = Path(__file__).parent.parent / "assets"

class WeatherApp:
    """Main GUI Application for Weather App."""

    def __init__(self, api_key: str):
        self.facade = WeatherFacade(api_key)
        self.root = CTk()
        self._setup_window()
        self._create_widgets()
        self._load_assets()

    def _setup_window(self) -> None:
        """Configure the main window."""
        self.root.geometry("800x500+300+200")
        self.root.title("Weather App")
        self.root.config(bg="#E3F3FD")
        self.root.resizable(False, False)

    def _load_assets(self) -> None:
        """Load and set window icon."""
        logo_path = ASSETS_DIR / "logo.png"
        if logo_path.exists():
            from PIL import ImageTk
            self.logo_icon = ImageTk.PhotoImage(Image.open(logo_path))
            self.root.iconphoto(False, self.logo_icon)
            self.root.after(250, lambda: self.root.iconphoto(False, self.logo_icon))

    def _create_widgets(self) -> None:
        """Create and place UI widgets."""
        # User input
        self.entry = CTkEntry(
            self.root, bg_color="#E3F3FD", fg_color="#E3F3FD",
            width=520, height=50, text_color="#404040"
        )
        self.entry.place(x=270, y=17)

        # Logo
        logo_img_path = ASSETS_DIR / "weather-app.png"
        if logo_img_path.exists():
            logo_image = Image.open(logo_img_path).resize((120, 120))
            self.logo_photo = CTkImage(logo_image, size=(120, 120))
            self.logo_label = CTkLabel(self.root, image=self.logo_photo, text="", bg_color="#E3F3FD")
            self.logo_label.place(x=250, y=150)

        # Search button
        search_icon_path = ASSETS_DIR / "search_icon.png"
        if search_icon_path.exists():
            search_icon = CTkImage(Image.open(search_icon_path), size=(30, 30))
            self.search_button = CTkButton(
                self.root, image=search_icon, text="", border_width=0,
                cursor="hand2", fg_color="#E3F3FD", bg_color="#E3F3FD",
                width=40, command=self._start_weather_thread, hover_color="#E3F3FD"
            )
            self.search_button.place(x=740, y=23)

        # Labels for display
        self.city_label = CTkLabel(self.root, font=('Arial', 15, 'bold'), text_color="#404040", bg_color="#E3F3FD")
        self.city_label.place(x=30, y=100)
        self.clock_label = CTkLabel(self.root, font=('Helvetica', 20), text_color="#404040", bg_color="#E3F3FD")
        self.clock_label.place(x=30, y=130)

        self.temp_label = CTkLabel(self.root, font=('Arial', 70, 'bold'), text_color="#ee666d", bg_color="#E3F3FD")
        self.temp_label.place(x=400, y=150)
        self.cond_label = CTkLabel(self.root, font=('Arial', 15, 'bold'), text_color="#000000", bg_color="#E3F3FD")
        self.cond_label.place(x=400, y=250)

        # Weather details frame
        self.bottom_frame = CTkFrame(self.root, width=750, height=100, corner_radius=20, fg_color="#1ab5ef", bg_color="#E3F3FD")
        self.bottom_frame.place(x=40, y=380)

        self._create_detail_labels()

    def _create_detail_labels(self) -> None:
        """Create labels for wind, humidity, description, and pressure."""
        notes = ["WIND", "HUMIDITY", "DESCRIPTION", "PRESSURE"]
        icon_names = ["wind.png", "humidity.png", "description.png", "pressure.png"]

        self.detail_labels: dict[str, CTkLabel] = {}
        for i, (note, icon_name) in enumerate(zip(notes, icon_names)):
            icon_path = ASSETS_DIR / icon_name
            if icon_path.exists():
                icon_image = Image.open(icon_path).resize((40, 40))
                icon_photo = CTkImage(icon_image)
                label = CTkLabel(
                    self.root, text=note, image=icon_photo, compound="left",
                    font=("Helvetica", 15, 'bold'), text_color="#ffffff",
                    bg_color="#1ab5ef", padx=5, pady=5
                )
                label.place(x=60 + i * 200, y=390)
                self.detail_labels[note] = label

        self.wind_val = CTkLabel(self.root, text="", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
        self.wind_val.place(x=80, y=430)
        self.hum_val = CTkLabel(self.root, text="", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
        self.hum_val.place(x=300, y=430)
        self.desc_val = CTkLabel(self.root, text="", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
        self.desc_val.place(x=500, y=430)
        self.press_val = CTkLabel(self.root, text="", font=('Arial', 15, 'bold'), bg_color="#1ab5ef")
        self.press_val.place(x=700, y=430)

    def _start_weather_thread(self) -> None:
        """Start a new thread to fetch weather data."""
        threading.Thread(target=self._update_weather).start()

    def _update_weather(self) -> None:
        """Fetch and update weather information in the UI."""
        city = self.entry.get().strip()
        if not city:
            CTkMessagebox(title="Warning", message="Please enter a city name!", icon="warning")
            return

        weather = self.facade.get_weather_info(city)
        if not weather:
            CTkMessagebox(title="Error", message="Could not fetch weather data. Check city name or connection.", icon="cancel")
            return

        self._display_weather(weather)

    def _display_weather(self, weather: WeatherData) -> None:
        """Update the UI with the provided weather data.

        Args:
            weather: The WeatherData object to display.
        """
        self.city_label.configure(text=f"Your city: {weather.city}")
        self.clock_label.configure(text=weather.local_time.strftime("%H:%M:%S \n%Y/%m/%d"))
        self.temp_label.configure(text=f"{weather.temp}°C")
        self.cond_label.configure(text=f"{weather.condition} | FEELS LIKE {weather.temp}°C")
        self.wind_val.configure(text=f"{weather.wind_speed} m/s")
        self.hum_val.configure(text=f"{weather.humidity}%")
        self.desc_val.configure(text=weather.description.capitalize())
        self.press_val.configure(text=f"{weather.pressure} hPa")

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
