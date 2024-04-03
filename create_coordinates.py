import googlemaps
import pandas as pd

# Define data
data = {
    'id': [1, 2, 3, 4, 5],
    'country': ['kosovo', 'kosovo', 'kosovo', 'kosovo', 'kosovo'],
    'city': ['gjakova', 'peja', 'pristina', 'prizren', 'mitrovica']
}
# Create DataFrame
df = pd.DataFrame(data)

api_key = 'AIzaSyAmgeYmB770rHsh55nefOgpEWRXFTpaA1Q'
gmaps = googlemaps.Client(key=api_key)

# Create a new column for coordinates
df['coordinates'] = ''

# Iterate over DataFrame rows
for row in df.itertuples():
    geocode_result = gmaps.geocode(f"{row.city}, {row.country}")
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    df.at[row.Index, 'coordinates'] = (latitude, longitude)

# Print DataFrame
print(df)
