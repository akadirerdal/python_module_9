"""Exercise 0: basic Pydantic model for space station data."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """A station report. Field() sets the length and range limits."""

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Not operational"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def display_errors(error: ValidationError) -> None:
    for detail in error.errors():
        print(detail["msg"])


def main() -> None:
    """Create a valid station, then show the error for an invalid one."""
    separator = "=" * 40
    station_data: dict[str, Any] = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2024-01-15T10:30:00",
    }
    overcrowded_data: dict[str, Any] = {**station_data, "crew_size": 25}

    print("Space Station Data Validation")
    print(separator)
    try:
        station = SpaceStation(**station_data)
        print("Valid station created:")
        display_station(station)
    except ValidationError as error:
        display_errors(error)

    print()
    print(separator)
    print("Expected validation error:")
    try:
        SpaceStation(**overcrowded_data)
        print("No validation error was raised")
    except ValidationError as error:
        display_errors(error)


if __name__ == "__main__":
    main()
