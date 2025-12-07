import os
import re
import sqlite3
from pathlib import Path
import PyPDF2
from datetime import datetime

def crear_base_datos():
    conn = sqlite3.connect('facturas.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            numero_paginas INTEGER NOT NULL,
            cufe TEXT,
            peso_archivo INTEGER NOT NULL,
            fecha_procesamiento TEXT
        )
    ''')
    
    conn.commit()
    return conn

def obtener_info_pdf(ruta_archivo):
    info = {
        'nombre': os.path.basename(ruta_archivo),
        'paginas': 0,
        'cufe': None,
        'peso': os.path.getsize(ruta_archivo)
    }
    
    try:
        with open(ruta_archivo, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            info['paginas'] = len(pdf_reader.pages)
            
            texto_completo = ''
            for page in pdf_reader.pages:
                texto_completo += page.extract_text()
            
            texto_limpio = texto_completo.replace('\n', '')
         
            patron_cufe = r'\b([0-9a-fA-F]{95,100})\b'#expresion regular
            match = re.search(patron_cufe, texto_limpio)
            
            if match:
                info['cufe'] = match.group(1)
            else:
                
                patron_cufe_con_saltos = r'\b([0-9a-fA-F]\n*){95,100}\b'
                match = re.search(patron_cufe_con_saltos, texto_completo)
                if match:
                  
                    cufe_raw = match.group(0)
                    info['cufe'] = re.sub(r'\s+', '', cufe_raw)
    
    except Exception as e:
        print(f"Error procesando {info['nombre']}: {str(e)}")
    
    return info

def procesar_facturas(directorio_pdfs):
    conn = crear_base_datos()
    cursor = conn.cursor()
    
    
    ruta = Path(directorio_pdfs)
    archivos_pdf = list(ruta.glob('*.pdf'))
    
    if not archivos_pdf:
        print(f"No se encontraron archivos PDF en {directorio_pdfs}")
        return
    
    print(f"Procesando {len(archivos_pdf)} archivos PDF...\n")
    
    for archivo in archivos_pdf:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Procesando: {archivo.name}")
        info = obtener_info_pdf(str(archivo))
        
        cursor.execute('''
                        INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo, fecha_procesamiento)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (info['nombre'], info['paginas'], info['cufe'], info['peso'], fecha_actual))
        
        print(f"  - Páginas: {info['paginas']}")
        print(f"  - Peso: {info['peso']:,} bytes")
        print(f"  - CUFE: {info['cufe'][:50] + '...' if info['cufe'] else 'No encontrado'}")
        print()
    
    conn.commit()
    

    print("=" * 70)
    print("RESUMEN DE PROCESAMIENTO")
    print("=" * 70)
    
    cursor.execute('SELECT COUNT(*) FROM facturas')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM facturas WHERE cufe IS NOT NULL')
    con_cufe = cursor.fetchone()[0]
    
    print(f"Total de facturas procesadas: {total}")
    print(f"Facturas con CUFE extraído: {con_cufe}")
    print(f"Facturas sin CUFE: {total - con_cufe}")
    print(f"\nDatos guardados en: facturas.db")
    
    conn.close()

def mostrar_resultados():
    try:
        conn = sqlite3.connect('facturas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT nombre_archivo, numero_paginas, cufe, peso_archivo 
            FROM facturas 
            ORDER BY nombre_archivo
        ''')
        
        print("\n" + "=" * 70)
        print("RESULTADOS ALMACENADOS EN LA BASE DE DATOS")
        print("=" * 70 + "\n")
        
        for row in cursor.fetchall():
            nombre, paginas, cufe, peso = row
            print(f"Archivo: {nombre}")
            print(f"  Páginas: {paginas}")
            print(f"  Peso: {peso:,} bytes ({peso/1024:.2f} KB)")
            if cufe:
                print(f"  CUFE: {cufe}")
            else:
                print(f"  CUFE: No encontrado")
            print()
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")

if __name__ == '__main__':
  
    directorio = './facturas'
    
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        print("Por favor, crea el directorio y coloca los archivos PDF allí.")
    else:
        procesar_facturas(directorio)
        mostrar_resultados()