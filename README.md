# 🕹️ GoFoodFL Tampa Eats

An ultra-lightweight, arcade-style app that turns the agonizing decision of picking where to eat into a retro arcade game.


## Features

* **Dynamic Canvas Wheel:** 
    Generates custom slices and text rendering programmatically with smooth deceleration physics.
* **Live Geolocation:** 
    Integrates browser location APIs to detect user coordinate points in real time.
* **Mobile Responsive Design:** 
    Built with compact, fixed constraints tailored specifically for smartphone screens.
* **Distance Filtering:** 
    Automatically processes a local dataset of 1,290+ restaurants to select and load the 24 closest options.
* **Integrated Micro-Map:** 
    Uses Leaflet.js and OpenStreetMap to display a map and place a custom marker on your final dining destination for quick navigation.


## Tech Stack

| Component | Technology | Engineering Impact |
| :--- | :--- | :--- |
| **Ingestion (ELT)** | Python 3 + Requests | Extracts raw, unstructured geospatial data from the Overpass API. |
| **Pipeline Logic** | Python (OS, JSON) | Cleans corrupt records, standardizes coordinates, and enforces a strict schema. |
| **Storage Layer** | Decoupled JSON | Replaced a traditional database server with a static asset to ensure zero-cost, instant mobile delivery. |
| **Validation Layer** | HTML5 / Leaflet.js | Built a lightweight UI strictly to validate pipeline output and end-to-end data integrity. |


## Pipeline

The project splits workflows into an execution engine (`maineats.py`) and a configuration manager (`build_datafood.py`).

* **The Engine (`maineats.py`):** Does all the heavy lifting. Fetches and cleans raw geospatial data based on passed coordinates.
* **The Controller (`build_datafood.py`):** The central config file where you set your target location and radius parameters.
* **Multi-Region Scaling:** To pull data for a new city, just append its coordinates to the controller file without changing any core logic.
* **Idempotent Output:** Every run overwrites the old JSON asset, ensuring fresh data with zero duplication or lag.

```python
# To change regions or scale horizontally, modify the parameters in build_datafood.py:
maineats.download_region_data(
    lat=28.0500, 
    lon=-82.4000, 
    radius=35000, 
    output_path="../data/gofoodfl.json"
)
```

## Quick Start & Installation

### Prerequisites

* Python 3.
* **Live Server** extension by Ritwick Dey installed in VS Code (or Python's built-in `http.server`).

### Step-by-Step Installation

1. **Clone the repository to your machine:**
```bash
git clone [https://github.com/rcug/gofoodfl.git](https://github.com/rcug/gofoodfl.git)
cd gofood

```

2. **Install dependencies:**
```bash
pip install requests

```

3. **Generate or update your local dataset:**
Modify coordinates inside `build_datafood.py` if desired, then execute the script:
```bash
python build_datafood.py

```

4. **Launch the web application:**
Open the project folder in VS Code, click **Go Live** on the bottom status bar to launch the Live Server extension, and open the app on your browser.


## Live Demo

You can access the live application here: [Launch GoFoodFL Arcade](https://rcug.github.io/gofoodfl/gofoodfl.html)

```

```