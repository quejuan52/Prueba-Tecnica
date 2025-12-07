# Prueba-Tecnica

Este repositorio contiene dos desarrollos independientes utilizando Django y python.

## Proyecto Django-Validación de archivo CSV

Este proyecto permite subir un archivo CSV y valida su estructura siguiendo los siguientes criterios:

### ✅ Requerimientos de validación
-El archivo debe contener exactamente 5 columnas, si existe mas o menos deberá alertar al usuario
-Columna 1: Solo números enteros entre 3 y 10 dígitos.
-Columna 2: Debe ser un correo electrónico válido.
-Columna 3: Solo permite los valores "CC" o "TI".
-Columna 4: Solo valores numéricos entre 500000 y 1500000.
-Columna 5: Acepta cualquier valor.

Si alguna regla falla, el sistema muestra los errores detallados por fila y columna.

### 🛠 Tecnologias Utilizadas

-Python 3.10+
-Django 5+
-HTML + TailwindCSS (interfaz)
-Regex para validaciones
-Manejo de archivos CSV

### ▶ pasos para ejecutar el script de PDFs

1. Crear el entorno virtual
    - python -m venv venv
2. Ejecutar migraciones
    - py manage.py migrate
3. Navegar a la carpeta principal del proyecto 
    - cd validaciones/
4.  Una vez en la carpeta del proyecto ejecutar el servidor
    - py manage.py runserver
5. La aplicacion se abrira en
    - http://127.0.1:8000


## Proyecto Python-Extracción de CUFE desde PDFs

Este script procesa archivos PDF y extrae el CUFE usando la expresion regular

(\b([0-9a-fA-F]\n*){95,100}\b)

cada factura se guarda en una base de datos SQlite como se observa en la tabla:

| Campo               | Descripción       |
| ------------------- | ----------------- |
| nombre_archivo      | Nombre del PDF    |
| numero_paginas      | Total de páginas  |
| cufe                | CUFE encontrado   |
| peso_archivo        | Tamaño en bytes   |
| fecha_procesamiento | Fecha de registro |

### 🛠 Tecnologias Utilizadas
-Python 3.10+
-PyPDF2 para lectura de PDFs
-Regex para extracción del CUFE
-SQLite3 para almacenamiento
-Pathlib + OS para manejo de archivos

### ▶ pasos para ejecutar el script de PDFs

1. Crear el entorno virtual
    - python -m venv venv
2. Navegar a la carpeta principal del script 
    - cd pdf_extraccion_info/
3. Una vez en la carpeta del script ejecutar el script
    - py extractor.py


