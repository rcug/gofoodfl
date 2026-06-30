import os
import json
import requests

def get_local_eats_radius(lat, lon, radius_meters=35000):
    overpass_url = "https://overpass-api.de/api/interpreter"
    contact_info = os.getenv("APP_CONTACT_EMAIL", "anonymous357@example.com")
    user_agent = f"FriendsEatApp/1.0 (contact: {contact_info})"

    query = f"""[out:json][timeout:90];
        (
          nwr["amenity"="restaurant"](around:{radius_meters},{lat},{lon});
          nwr["amenity"="cafe"](around:{radius_meters},{lat},{lon});
          nwr["amenity"="pub"](around:{radius_meters},{lat},{lon});
        );
        out center;"""
    
    headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    response = requests.post(overpass_url, data={"data": query}, headers=headers, timeout=120)
    response.raise_for_status() 
    return response.json()

def parse_osm_data(raw_data):
    cleaned_places = []
    for element in raw_data.get("elements", []):
        tags = element.get("tags", {})
        if "name" not in tags:
            continue
            
        cleaned_places.append({
            "name": tags.get("name"),
            "type": tags.get("amenity"),
            "cuisine": tags.get("cuisine", "Not Specified"),
            "latitude": element.get("lat") or element.get("center", {}).get("lat"),
            "longitude": element.get("lon") or element.get("center", {}).get("lon"),
            "website": tags.get("website"),
        })
    return cleaned_places

def download_region_data(lat, lon, radius, output_path):
    """Fetches, parses, and saves OSM data for any given coordinate set."""
    try:
        print(f"Fetching data for location ({lat}, {lon})...")
        raw_osm = get_local_eats_radius(lat, lon, radius)
        restaurants = parse_osm_data(raw_osm)
        
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(restaurants, f, indent=4, ensure_ascii=False)
            
        print(f"Success: Localized database seeded at '{output_path}' Found ({len(restaurants)} restaurants).\n")
    except Exception as e:
        print(f"Failed to process location ({lat}, {lon}): {e}\n")
