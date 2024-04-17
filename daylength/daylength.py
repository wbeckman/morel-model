from datetime import date, timedelta
from astral.sun import sun
from astral.location import LocationInfo
import pytz

def compute_day_length(latitude, longitude, date_input):
    try:
        location = LocationInfo(latitude=latitude, longitude=longitude)

        # Calculate sunrise and sunset times using UTC to avoid timezone issues
        s = sun(location.observer, date=date_input, tzinfo=pytz.utc)

        # Calculate day length
        sunrise = s['sunrise']
        sunset = s['sunset']
        day_length = sunset - sunrise

        # Correct day_length if it's negative by setting day component to zero
        if day_length.days < 0:
            # Reset days to 0 and preserve only the time portion
            day_length = timedelta(hours=day_length.seconds // 3600,
                                   minutes=(day_length.seconds // 60) % 60,
                                   seconds=day_length.seconds % 60)
        return day_length
    except Exception:
        return None

if __name__ == '__main__':
    latitude = 40.7128  # New York City
    longitude = -74.0060
    date_of_interest = date(2023, 5, 25)  # May 25, 2023

    day_length = compute_day_length(latitude, longitude, date_of_interest)
    print("Day Length:", day_length)
