import pandas as pd
from pathlib import Path
from datetime import datetime

def clean_data(raw_path: Path, config):
    processed_dir = Path(config["paths"]["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("🧹 Limpiando y FILTRANDO solo año 2025...")
    df = pd.read_csv(raw_path, chunksize=config["processing"]["chunk_size"], low_memory=False)
    cleaned_chunks = []
    
    for chunk in df:
        chunk["periodo"] = pd.to_datetime(chunk["periodo"], format="%Y%m%d", errors="coerce")
        for col in config["processing"]["numeric_columns"]:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")
        
        # Filtramos solo 2025 (para que el archivo final sea ligero)
        chunk_2025 = chunk[chunk["periodo"].dt.year == 2025]
        cleaned_chunks.append(chunk_2025)
    
    final_df = pd.concat(cleaned_chunks, ignore_index=True)
    parquet_path = processed_dir / f"cuipo_2025_clean_{datetime.now().strftime('%Y%m%d')}.parquet"
    final_df.to_parquet(parquet_path, compression="zstd", index=False)
    print(f"✅ Datos limpios de 2025 guardados: {parquet_path}")
    print(f"   (Archivo ligero ≈ 80-120 MB - listo para Excel/Power BI)")
    return parquet_path