import os
import json
import requests

def get_local_eats_radius(lat, lon, radius_meters):
    overpass_url = "https://overpass-api.de/api/interpreter"
    contact_info = os.getenv("APP_CONTACT_EMAIL", "anonymous579@example.com")
    user_agent = f"FriendsEatApp/1.0 (contact: {contact_info})"

    query = f"""[out:json][timeout:120];
        (
        node["amenity"~"restaurant|fast_food|cafe|food_court|bar|pub|ice_cream|street_food"](around:{radius_meters},{lat},{lon});
        node["cuisine"~"padang|indonesian|noodle|bakso|chicken|ayam|street_food|sate|soto|warung|pecel|kantin|warteg|warkop"](around:{radius_meters},{lat},{lon});
        node["shop"="bakery"](around:{radius_meters},{lat},{lon});
        way["amenity"~"restaurant|fast_food|cafe|food_court|bar|pub|ice_cream|street_food"](around:{radius_meters},{lat},{lon});
        way["cuisine"~"padang|indonesian|noodle|bakso|chicken|ayam|street_food|sate|soto|warung|pecel|kantin|warteg|warkop"](around:{radius_meters},{lat},{lon});
        way["shop"="bakery"](around:{radius_meters},{lat},{lon});
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
    blacklist = ["public_building", "internet_cafe",
        "kantor", "office", "bank", "atm", "masjid", "musholla", "church", "gereja", 
        "school", "sekolah", "university", "universitas", "univ", "sd", "smp", "sma" ]
    
    for element in raw_data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name", "").strip()
        if not name:
            continue
        name_lower = name.lower()
        type_lower = (tags.get("amenity") or "").lower()
        if any(keyword in name_lower or keyword in type_lower for keyword in blacklist):
            continue
            
        cleaned_places.append({
            "name": name,
            "type": tags.get("amenity"),
            "cuisine": tags.get("cuisine", "Not Specified"),
            "latitude": element.get("lat") or element.get("center", {}).get("lat"),
            "longitude": element.get("lon") or element.get("center", {}).get("lon"),
            "website": tags.get("website"),
        })
    sorted_places = sorted(
        cleaned_places, 
        key=lambda x: (x.get("latitude") or 0.0, x.get("longitude") or 0.0, x.get("name").lower())
    )
    return sorted_places

def download_region_data(lat, lon, radius, output_path):
    """Fetches, parses, and saves OSM data for any given coordinate set."""
    try:
        print(f"Fetching data for location ({lat}, {lon}) with radius {radius}m...")
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
