import requests



def geocode_address(address, api_key):
    """
    Given an address and an API key, this function returns the latitude
    and longitude of the address using the Google Maps Geocoding API.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            # Extract the first result's location data
            location = data["results"][0]["geometry"]["location"]
            return location
        else:
            print("Error from API:", data["status"])
    else:
        print("HTTP error:", response.status_code)
    return None

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Google API key
    api_key = "AIzaSyCXKyniEpWy06qPM-3fjf0fTDk6P_NH7G8"
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    location = geocode_address(address, api_key)
    if location:
        print("Latitude:", location["lat"])
        print("Longitude:", location["lng"])
    else:
        print("Failed to get geolocation data.")
