from src.config_loader import load_config
from src.data_checker import has_new_data
from src.extractor import download_full_csv
from src.processor import clean_data
import json
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, 
                    filename="logs/cuipo_automation.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    config = load_config()
    print("Iniciando verificación CUIPO - Observatorio Fiscal Javeriana")
    
    if has_new_data(config):
        print(" Se detectaron nuevos datos")
        raw_path = download_full_csv(config)
        parquet_path = clean_data(raw_path, config)
        
        meta = {
            "rowsUpdatedAt": requests.get(config["urls"]["metadata_url"]).json()["rowsUpdatedAt"],
            "last_run": datetime.now().isoformat()
        }
        with open(config["paths"]["last_update_file"], "w") as f:
            json.dump(meta, f)
        print(" ¡Proceso completo! Revisa data/processed/")
    else:
        print("No hay datos nuevos esta vez")
