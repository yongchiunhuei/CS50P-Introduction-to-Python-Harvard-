# SARA: Tesla Mission Control & Route Auditor

#### Video Demo: [https://youtu.be/udnZYoU_qzM]

## Project Overview
**SARA (Sync, Audit, Route, Autonomy)** is a Python-based mission control interface designed for the **Tesla Model 3/Y Long Range** rover. The primary objective of this project is to solve "range anxiety" by performing a real-time Logic-Sync between the vehicle's current State of Charge (SOC) and the intended target destination. 

Unlike standard navigation apps, SARA performs a pre-flight energy audit. If the system detects that the battery levels will fall below a critical 10% safety buffer, it automatically triggers a "Sector Recovery" protocol, harvesting nearby Tesla Supercharger locations from the Google Cloud data-grid and injecting them as mandatory waypoints into the navigation path.

## File Architecture

### 1. `project.py`
This is the heart of the Mission Control. It utilizes four main functional blocks:
- **`get_route_options`**: Connects to the Google Directions API to acquire multiple tactical paths to the destination. It converts raw meter data into kilometers for the energy audit.
- **`audit_mission`**: The mathematical engine. It calculates energy consumption based on a 75kWh battery capacity and a 6.5km/kWh efficiency constant. It returns a boolean "GO/ABORT" status and the predicted arrival SOC.
- **`handle_recharge`**: The emergency protocol. If the audit fails, this function uses the Google Places API and Distance Matrix API to find and rank the three nearest charging targets.
- **`launch_navigation`**: The execution layer. It uses URL encoding to synthesize a final Google Maps link, ensuring all locations and waypoints are "sanitized" for web transmission.

### 2. `test_project.py`
To ensure Magnitude 1,000,000 reliability, this file utilizes the `pytest` framework. It employs "Mocking" techniques to simulate API responses, allowing the system to be audited without consuming live Google Cloud credits or requiring a satellite link. It tests the energy math, the URL generation, and the error-handling logic.

### 3. `requirements.txt`
This file ensures that the `requests` library—our primary link to the Google API ecosystem—is correctly installed in the grading environment.

## Design Choices & Constants
- **Safety Buffer**: A hardcoded 10% reserve was chosen to account for "Vampire Drain" and environmental factors in Aachen, Germany, such as cold weather or high-speed Autobahn travel.
- **API Choice**: The project integrates three distinct Google APIs (Directions, Places, and Distance Matrix) to provide a more holistic data-sync than a single API could offer.
- **Vehicle Profile**: The constants are tuned to the Tesla Model 3/Y Long Range (75kWh usable), providing the most accurate results for the most common rover models in the current ecosystem.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Execute the mission: `python project.py`
3. Enter your departure, destination, and current battery percentage when prompted.

## Technical Challenges & Future Missions
During the development of the SARA system in the Aachen-Sanctuary, several 
"Magnitude Errors" were identified and overcome. The primary challenge was 
synchronizing the Google Directions API with the custom energy audit math. 
Since the API returns distances in meters, the system had to perform a 
precision conversion to kilometers before applying the 6.5km/kWh efficiency 
constant. 

In future iterations, SARA could be upgraded to account for real-time 
environmental data, such as elevation changes or wind speed, which 
significantly impact the Tesla's range. Additionally, the "Sector Recovery" 
protocol could be expanded to include non-Tesla charging networks, 
increasing the rover's autonomy in remote sectors.
