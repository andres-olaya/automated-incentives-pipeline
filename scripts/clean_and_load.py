import pandas as pd
import os
from datetime import datetime

# Carpetas donde están los archivos
RAW_FOLDER = "../data/raw/"
PROCESSED_FOLDER = "../data/processed/"

def clean_data(df):
    # Normalizo los nombres de columna
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convierto columnas clave si existen
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if 'incentive' in df.columns:
        df['incentive'] = pd.to_numeric(df['incentive'], errors='coerce')

    # Extraigo el mes si hay fechas
    if 'date' in df.columns:
        df['month'] = df['date'].dt.to_period('M')

    # Sumo incentivos si están las columnas necesarias
    if {'base_incentive', 'bonus'}.issubset(df.columns):
        df['total_incentive'] = df['base_incentive'] + df['bonus']

    return df

def process_files():
    # Recorro todos los archivos con extensión .xlsx o .csv en la carpeta RAW
    files = [f for f in os.listdir(RAW_FOLDER) if f.endswith(('.xlsx', '.csv'))]

    for file in files:
        print(f"Procesando: {file}")

        path = os.path.join(RAW_FOLDER, file)

        # Leo según el tipo de archivo
        if file.endswith('.xlsx'):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)

        df_clean = clean_data(df)

        output_name = f"processed_{file.split('.')[0]}.csv"
        output_path = os.path.join(PROCESSED_FOLDER, output_name)

        # Guardo el archivo limpio
        df_clean.to_csv(output_path, index=False)
        print(f"Guardado en: {output_path}")

if __name__ == "__main__":
    process_files()
