import pandas as pd
import papermill as pm
import sys

def load_config(config_file='config.py'):
    """Carga la configuración desde el archivo config.py."""
    import config  # Importa el archivo como módulo
    return {"symbols": config.symbols, "frequencies": config.frequencies, "window": config.window_pred}

def load_data(config):
    """Carga los datos de todas las monedas para cada frecuencia."""
    symbols = config['symbols']  # Lista de monedas (ej. ["BTCUSDT", "ETHUSDT"])
    frequencies = config['frequencies']  # Lista de frecuencias (ej. ["1h", "4h", "1d"])
    window = config['window']  # tamaño de ventana
    
    data_by_freq = {}

    for freq in frequencies:
        dfs = []
        for symbol in symbols:
            file_name = f"{symbol}_{freq}_01-01-2016_01-01-2025.csv"
            df = pd.read_csv(file_name, index_col='timestamp')
            df = df[['close']].rename(columns={'close': f'{symbol}_{freq}'})  # Renombrar columna para evitar conflictos
            dfs.append(df)
        
        # Unir todas las monedas por frecuencia en un único DataFrame
        data_by_freq[freq] = pd.concat(dfs, axis=1)
        data_by_freq[freq].dropna(inplace=True)  # Eliminar filas con NaN en alguna moneda
    
    return data_by_freq, window


def run_notebook(freq, window):
    print(f"Ejecutando notebook GLOBAL para frecuencia {freq} y window {window} con {len(df.columns)} activos...")

    # Ejecutar el notebook con el parámetro 'frequency'
    pm.execute_notebook(
        'global.ipynb',  # El archivo del notebook
        'output_notebook_global.ipynb',  # El archivo de salida (puedes usar el mismo o diferente)
        parameters={'frequency': freq, 'window_pred': window}  # Pasar el valor de 'frequency'
    )


def save_results(results, output_file="final_accuracy_results_glob.csv"):
    """Guarda los resultados en un archivo CSV."""
    df = pd.DataFrame(results, columns=['Frequency', 'Asset', 'Model', 'Accuracy', 'Vald/Test'])
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    config = load_config()
    data_by_freq, window = load_data(config)

    results = []

    for freq, df in data_by_freq.items():
        df.to_csv(f"processed_data_{freq}_glob.csv")
        # Ejecutar el notebook solo una vez por frecuencia
        run_notebook(freq, window)
        print(f"Ejecutado el notebook")
        # Leer el archivo generado por el notebook
        acc_file = f'accuracy_results_{freq}_glob.csv'
        acc_data = pd.read_csv(acc_file)

        for _, row in acc_data.iterrows():
            results.append([freq, row['Asset'], row['Model'], row['Accuracy'], row['What']])
    
    # Guardar los resultados finales
    save_results(results)
    print("Proceso completado. Saliendo...")
    sys.exit() 