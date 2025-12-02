from sqlalchemy.orm import Session

# --- UPDATED IMPORTS ---
# We import the classes from their specific files now
# Note: Ensure the folder "backend" actually exists inside "app". 
# If your path is actually "app/models/cargo_master.py", remove ".backend" below.
from app.models.cargo_master import CargoTankMaster
from app.models.regulations_master import RegulationsMaster

def init_seed_data(db: Session):
    """
    Checks if tables are empty and populates them with initial 5 values.
    """
    
    # --- 1. Seed CargoTankMaster ---
    try:
        if not db.query(CargoTankMaster).first():
            print("Seeding CargoTankMaster data...")
            
            cargo_tanks = [
                CargoTankMaster(cargo_reference="CT-Alpha-01"),
                CargoTankMaster(cargo_reference="CT-Bravo-02"),
                CargoTankMaster(cargo_reference="LNG-Storage-05"),
                CargoTankMaster(cargo_reference="LPG-Transport-09"),
                CargoTankMaster(cargo_reference="Chem-Residue-X1"),
            ]
            
            db.add_all(cargo_tanks)
            db.commit()
            print("CargoTankMaster seeded successfully.")
        else:
            print("CargoTankMaster data already exists. Skipping.")

    except Exception as e:
        print(f"Error seeding CargoTankMaster: {e}")
        db.rollback()

    # --- 2. Seed RegulationsMaster ---
    try:
        if not db.query(RegulationsMaster).first():
            print("Seeding RegulationsMaster data...")
            
            regulations = [
                RegulationsMaster(regulation_name="API Standard 650"),
                RegulationsMaster(regulation_name="ISO 9001:2015"),
                RegulationsMaster(regulation_name="OSHA 1910.119"),
                RegulationsMaster(regulation_name="MARPOL Annex I"),
                RegulationsMaster(regulation_name="ASME Section VIII"),
            ]
            
            db.add_all(regulations)
            db.commit()
            print("RegulationsMaster seeded successfully.")
        else:
            print("RegulationsMaster data already exists. Skipping.")

    except Exception as e:
        print(f"Error seeding RegulationsMaster: {e}")
        db.rollback()