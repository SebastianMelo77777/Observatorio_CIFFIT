import requests
from pathlib import Path
from datetime import datetime

def download_full_csv(config):
    """Descarga completa estable (la que siempre funciona)"""
    url = config["urls"]["csv_export_url"]   # ← URL oficial y estable
    raw_dir = Path(config["paths"]["raw_dir"])
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"cuipo_completo_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = raw_dir / filename
    
    print("⏳ Descargando dataset COMPLETO (~14 millones de filas, 3-5 minutos)...")
    print("   (Esta es la URL más estable de datos.gov.co)")
    resp = requests.get(url, stream=True, timeout=600)
    resp.raise_for_status()
    
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Descarga terminada: {filepath}")
    return filepath