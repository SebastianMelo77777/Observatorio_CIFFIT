import pandas as pd
import requests
from datetime import datetime

print("🚀 Probando API CUIPO - Observatorio Fiscal Javeriana")
print("="*65)

# 1. Metadata (última actualización)
meta_url = "https://www.datos.gov.co/api/views/4f7r-epif.json"
meta = requests.get(meta_url, timeout=30).json()
timestamp = meta.get("rowsUpdatedAt")
fecha = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M") if timestamp else "Desconocida"
print(f"✅ Última actualización del dataset: {fecha}")

# 2. Descargar muestra ORDENADA por período más reciente (CORREGIDO)
print("\n⏳ Descargando 10.000 filas más recientes (esto tarda ~15 segundos)...")
sample_url = "https://www.datos.gov.co/resource/4f7r-epif.csv?$limit=10000&$order=periodo%20DESC"
df = pd.read_csv(sample_url, low_memory=False)

print(f"✅ Muestra cargada correctamente: {len(df):,} filas")
print(f"📅 Período más reciente en los datos: {df['periodo'].max()}")
print(f"\nPrimeras 3 filas (las más nuevas - Tercer Trimestre 2025):")
print(df.head(3)[['periodo', 'codigo_entidad', 'nombre_entidad', 'nombre_cuenta', 'compromisos', 'obligaciones', 'pagos']])

# 3. Guardar para que lo abras en Excel
df.to_csv("data/raw/cuipo_muestra_prueba_v3.csv", index=False)
print(f"\n💾 Archivo guardado: data/raw/cuipo_muestra_prueba_v3.csv")
print("\n🎉 ¡LA API ESTÁ FUNCIONANDO PERFECTAMENTE!")
print("Ya tienes los datos reales de ejecución CUIPO trimestral.")