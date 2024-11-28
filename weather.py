import requests
import geocoder
def get_location():
    # Use geocode to take retreive the weather data via IP or GPS 
    g = geocoder.ip('me')  # Get the position of a user via IP
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    #print("Latitude: ", latitude, "Longitude: ", longitude)
    return {
        'Latitude':latitude,
        'Longitude':longitude
    }
    
def get_weather_data():
    
    loc = get_location()
    lat = loc['Latitude']
    lon = loc['Longitude']
    
    api_key = '674d86b892da930e68d189d2a50f46f7'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=fr&appid={api_key}'
    
    response = requests.get(url)
    weather_data = response.json()
    
    #Extract useful info
    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp'] - 273 # Conversion from Kelvin to Celsius
    humidity = weather_data['main']['humidity'] # Humidity is express as a percentage 
    wind_speed = weather_data['wind']['speed'] # Default unit = meter/sec
    city = weather_data['name']
    
    return {
          'city' : city,
        'description' : description,
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind_speed
    }

if __name__ == "__main__":
    print(get_weather_data())