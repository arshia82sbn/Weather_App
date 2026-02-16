from dataclasses import dataclass

@dataclass(frozen=True)
class LocationData:
    """Data class for geographical location information."""
    name: str
    latitude: float
    longitude: float
