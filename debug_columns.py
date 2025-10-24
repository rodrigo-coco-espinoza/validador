"""
Script para depurar problemas con columnas
"""
import pandas as pd
from file_selector import FileSelector

def debug_columns():
    file_selector = FileSelector()
    
    # Solicitar archivo
    print("Seleccione el archivo que está causando problemas:")
    file_path = file_selector.select_file(title="Seleccione archivo para depurar")
    
    if not file_path:
        print("No se seleccionó ningún archivo")
        return
    
    # Cargar archivo
    print(f"Cargando archivo: {file_path}")
    df = file_selector.load_file(file_path)
    
    # Mostrar información del archivo ANTES de limpiar
    print(f"\n📁 Archivo: {file_path.split('/')[-1]}")
    print(f"📊 Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"\n📋 Columnas ORIGINALES:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. '{col}' (tipo: {df[col].dtype})")
    
    # Limpiar nombres de columnas (como hace el validador)
    df.columns = [col.strip().lstrip('\ufeff').lstrip('ï»¿') for col in df.columns]
    
    # Mostrar información del archivo DESPUÉS de limpiar
    print(f"\n📋 Columnas DESPUÉS DE LIMPIAR:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. '{col}' (tipo: {df[col].dtype})")
    
    # Verificar si existe 'RUT'
    if 'RUT' in df.columns:
        print(f"\n✅ La columna 'RUT' SÍ existe")
        print(f"📊 Información de la columna RUT:")
        print(f"   - Tipo de dato: {df['RUT'].dtype}")
        print(f"   - Valores únicos: {df['RUT'].nunique():,}")
        print(f"   - Valores nulos: {df['RUT'].isnull().sum()}")
        print(f"   - Primeros 5 valores: {df['RUT'].head().tolist()}")
    else:
        print(f"\n❌ La columna 'RUT' NO existe")
        
        # Buscar columnas similares
        similares = [col for col in df.columns if 'rut' in col.lower() or 'run' in col.lower()]
        if similares:
            print(f"🔍 Columnas similares encontradas: {similares}")
        else:
            print(f"🔍 No se encontraron columnas similares a 'RUT'")

if __name__ == "__main__":
    debug_columns()