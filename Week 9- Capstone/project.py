import sys
import requests
import webbrowser
import urllib.parse

# --- CONFIGURATION ---
# Target: Tesla Model 3/Y Long Range profile
API_KEY = "AIzaSyAsv9gcSJ-1JGUKObdR04UNekONzgqhgDU" 
VEHICLE_MODEL = "Tesla Model 3/Y Long Range"
TESLA_CAPACITY_KWH = 75.0
TESLA_EFFICIENCY_KM_KWH = 6.5 

def get_route_options(origin, destination):
    """Target Acquisition: Scan Google Maps for potential travel sectors."""
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={API_KEY}"
    r= requests.get(url).json()
    if r['status'] != 'OK':
        raise ValueError(f"Route logic-sync failed: {r.get('status')}")
    return r["routes"][:3]

def audit_mission(current_soc, distance_km):
    """Energy Audit: Calculates if battery levels meet safety margins."""
    required_kwh = distance_km / TESLA_EFFICIENCY_KM_KWH
    usable_kwh= current_soc / 100 * TESLA_CAPACITY_KWH
    final_soc = (usable_kwh - required_kwh) / TESLA_CAPACITY_KWH * 100
    # Safety Buffer: Required arrival SOC >= 10%
    return (final_soc >= 10), round(final_soc, 1)

def handle_recharge(origin, destination):
    """Sector Recovery: Harvests nearby Superchargers if SOC is critical."""
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Tesla+Supercharger+near+{origin}&key={API_KEY}"
    r= requests.get(search_url).json()

    if r.get('status') == 'OK':
        stations= r['results'][:3]
        print("\n--- CRITICAL SOC: SELECT CHARGING WAYPOINT ---")      

        station_choices = []
        for i, s  in enumerate(stations):
            name = s.get('name')
            address = s.get('formatted_address')

            # Distance Sync: Calculate road distance to each charger
            dist_url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={address}&key={API_KEY}'
            d_res = requests.get(dist_url).json()
            dist_text = d_res['rows'][0]['elements'][0]['distance']['text']

            print(f'[{i+1}] STATION: {name}')
            print(f'    ADDRESS: {address}')
            print(f'    DISTANCE FROM ORIGIN: {dist_text}\n')
            station_choices.append(address)

        try:
            choice = int(input('Select Sector (1-3) or 0 to Abort: '))
            if 0 < choice <= len(station_choices):
                launch_navigation(origin, destination, station_choices[choice-1])
            else:
                print('Logic-Sync: Mission Aborted by Master.')
                sys.exit()
        except ValueError:
            print('Magnitude Error: Invalid input sequence.')
    else:
        print('Audit Failure: No charging targets identified.')
        
def launch_navigation(origin, destination, waypoint=None):
    """Terminal Execution: Opens the digital portal to Google Maps."""
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {
        "origin": origin,
        "destination": destination,
        "travelmode": "driving"
    }

    if waypoint:
        params["waypoints"] = waypoint

    nav_url = f"{base_url}&{urllib.parse.urlencode(params)}"
    print(f"\nTargeting satellite link... Syncing to Navigation.")
    webbrowser.open(nav_url)

def main():
    print("---SARA TESLA MISSION CONTROL: ROUTE SYNC---")
    print(f"ACTIVE SYSTEM: {VEHICLE_MODEL}")
    print(f"CONFIG: {TESLA_CAPACITY_KWH}kWh | Efficiency: {TESLA_EFFICIENCY_KM_KWH}km/kWh")
    print("-"*46)

    try: 
        origin= input("Departure Location: ")
        destination= input("Target Destination: ")
        soc = float(input("Current Battery %: "))

        routes = get_route_options(origin, destination)

        # Primary Audit based on the first suggested route
        primary_dist = routes[0]["legs"][0]["distance"]["value"]/ 1000
        is_viable, arrival_soc = audit_mission(soc, primary_dist)

        if is_viable:
            print(f"\nSTATUS: GO FOR LAUNCH | Buffer: NOMINAL ({arrival_soc}%)")
            print("SELECT YOUR SECTOR (ROUTE):")
            for i, route in enumerate(routes):
                print(f"[{i+1}] via {route['summary']} ({route['legs'][0]['distance']['text']})")

            choice= int(input("\nEnter Choice (1-3): "))
            # Optimization: Using the specific destination for the chosen route
            launch_navigation(origin, destination)
        else: 
            print(f"\nSTATUS: ABORT | Buffer: CRITICAL ({arrival_soc}%)")
            handle_recharge(origin, destination)
        
    except Exception as e:
        print(f"Magnitude Error; {e}")

if __name__ == "__main__":
    main()


            


         
