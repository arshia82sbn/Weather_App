from weather_app.api.gui import WeatherApp

def main() -> None:
    """Entry point for the application."""
    # In a real app, this might come from an environment variable or config file
    api_key = "Your API Key"

    app = WeatherApp(api_key)
    app.run()

if __name__ == "__main__":
    main()
