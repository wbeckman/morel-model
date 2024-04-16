from astral import LocationInfo
from astral.sun import sun
from datetime import date


def compute_day_length(latitude, longitude, date):
    # Define the location
    location = LocationInfo(latitude=latitude, longitude=longitude)

    # Calculate sunrise and sunset
    s = sun(location.observer, date=date)

    # Compute day length
    sunrise = s['sunrise']
    sunset = s['sunset']
    day_length = sunset - sunrise

    return day_length


if __name__ == "__main__":
    # Example usage
    latitude = 40.7128  # New York City
    longitude = -74.0060
    date_of_interest = date(2024, 12, 25)  # April 21, 2024

    day_length = compute_day_length(latitude, longitude, date_of_interest)
    print("Day Length:", day_length)

