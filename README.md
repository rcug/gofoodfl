# 🕹️ GoFoodFL Tampa Eats

An ultra-lightweight, arcade-style app that turns the agonizing decision of picking where to eat into a retro arcade game.

<img width="384" height="544" alt="gofoodfl1" src="https://github.com/user-attachments/assets/a14a23b1-adf1-4c64-9cd0-fcb12104dbb9" />

## Features

* **Dynamic Canvas Wheel:** 
    Generates custom slices and text rendering.
* **Live Geolocation:** 
    Integrates browser location APIs to detect user coordinates.
* **Mobile Responsive Design:** 
    Built compact for smartphone screens.
* **Distance Filtering:** 
    Processes a local dataset of 1K+ restaurants to select and load the 24 closest options.
* **Integrated Micro-Map:** 
    Uses Leaflet.js and OpenStreetMap to display the map.


## Tech Stack

| Component | Technology | Engineering Impact |
| :--- | :--- | :--- |
| **Ingestion (ELT)** | Python 3 + Requests | Extracts raw, unstructured geospatial data from the Overpass API. |
| **Pipeline Logic** | Python (OS, JSON) | Cleans corrupt records and standardizes coordinates and schema. |
| **Storage Layer** | Decoupled JSON | Replaced database server with a static asset for zero-cost. |
| **Validation Layer** | HTML5 / Leaflet.js | Built a lightweight UI to validate output, an end-to-end data integrity. |


## Structure
```text
├── README.md
├── gofoodfl.html
├── data/
│   └── gofoodfl.json
└── src/
    ├── maineats.py
    └── build_datafood.py
```

## Pipeline

The project splits workflows into an execution engine (`maineats.py`) and a configuration manager (`build_datafood.py`).

* **`maineats.py`:** Does all the heavy lifting. Fetches and cleans raw geospatial data.
* **`build_datafood.py`:** The config file where you set your target location and radius parameters.
    * multi-region scaling: To pull data for a new city, just append its coordinates to the controller file.
    * idempotent output: Every run overwrites the old JSON asset, ensuring fresh data with zero duplication.

```python
# To change regions or scale horizontally, modify the parameters in build_datafood.py:
maineats.download_region_data(
    lat=28.0500, 
    lon=-82.4000, 
    radius=35000, 
    output_path="../data/gofoodfl.json"
)
```

## Quick Start 

### Prerequisites

*  <a href="https://www.python.org/downloads/" target="_blank">**Python 3**</a>.
*  <a href="https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer" target="_blank">**Live Server**</a> extension by Ritwick Dey (or Python's built-in `http.server`).

### Installation

1. **Clone the repository to your machine:**
```bash
git clone https://github.com/rcug/gofoodfl.git
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

You can access the live application here: <a href="https://rcug.github.io/gofoodfl/gofoodfl.html" target="_blank">Launch GoFoodFL Arcade</a>

🍔
