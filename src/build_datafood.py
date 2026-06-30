from datetime import datetime
import maineats 

def run_scheduled_ingestion():
    print(f"Pipeline Started: {datetime.now()}")
    
    # Target Region 1: Tampa Area
    RADIUS = 42000
    maineats.download_region_data(
        lat=28.0500, 
        lon=-82.4000, 
        radius=RADIUS, 
        output_path="../data/gofoodflx.json"
    )
    
    # Target Region 2: Austin, Texas 
    # maineats.download_region_data(
    #     lat=30.2672, 
    #     lon=-97.7431, 
    #     radius=20000, 
    #     output_path="../data/gofoodtx.json"
    # )

    print("Pipeline Successfully Completed")

if __name__ == "__main__":
    run_scheduled_ingestion()