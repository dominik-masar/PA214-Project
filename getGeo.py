import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Load the dataset
file_path = "./space_missions/Space_Corrected.csv"
df = pd.read_csv(file_path)

# Initialize geolocator
geolocator = Nominatim(user_agent="space_launch_mapper", timeout=5)

# Dictionary to store cached locations (avoid duplicate lookups)
location_cache = {}

def get_lat_lon(df_location):
    """Get latitude & longitude for a location, trying progressively smaller location names."""
    loc_parts = df_location.split(", ")

    # Try from full location down to just the last part
    for i in range(len(loc_parts), 0, -1):
        location = ", ".join(loc_parts[-i:])  # Take the last `i` parts
        
        if location in location_cache:
            print(f"🟢 Cached result: {location} → {location_cache[location]}")
            return location_cache[location]
        
        try:
            loc = geolocator.geocode(location)
            if loc:
                if i == 1:
                    print(f" only state found", sep=" ")
                print(f"✅ Found: {location} → {loc.latitude}, {loc.longitude}")
                location_cache[location] = (loc.latitude, loc.longitude)
                return loc.latitude, loc.longitude
            else:
                print(f"❌ Not found: {location}, trying a shorter version...")
        
        except GeocoderTimedOut:
            print("⚠️ Geocoding timeout. Skipping...")
    
    return None, None  # Return None if all attempts fail


def get_lat_lon_old(df_location):
    """Get latitude & longitude for a location, using cache to speed up."""
    loc_parts = df_location.split(", ")
    state = loc_parts[-1]
    location = ", ".join(loc_parts[-2:])

    if location in location_cache:
        return location_cache[location]
    
    try:
        loc = geolocator.geocode(location)

        if loc:
            print(1, location, "found: ", loc.latitude, loc.longitude)
            location_cache[location] = (loc.latitude, loc.longitude)
            return loc.latitude, loc.longitude
        else:
            print(0, location, "not found, searching for state", end="... ")
            loc = geolocator.geocode(state)
            if loc:
                print(state, "found:", loc.latitude, loc.longitude)
                location_cache[location] = (loc.latitude, loc.longitude)
                return loc.latitude, loc.longitude
            else:
                print("state not found")
    except GeocoderTimedOut:
        print("failed")
        #time.sleep(1)  # Wait and retry
        #return get_lat_lon(location)
    
    return None, None  # Return None if lookup fails

# Apply geocoding to unique locations
df[['Latitude', 'Longitude']] = df['Location'].apply(lambda loc: pd.Series(get_lat_lon(loc)))

# Save the updated dataset with coordinates
output_file = "space_with_geo.csv"
df.to_csv(output_file, index=False)

print(f"Dataset with coordinates saved as {output_file}")
