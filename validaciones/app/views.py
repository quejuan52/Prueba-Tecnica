from django.shortcuts import render
import csv
import io
import re
from django.shortcuts import render
from .forms import UploadFileForm

def validar_archivo(request):
    errors = []
    success = False

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["file"]

            data = file.read().decode("utf-8")
            reader = csv.reader(io.StringIO(data), delimiter=",")

            row_num = 0

            for row in reader:
                row_num += 1

                if len(row) != 5:
                    errors.append(f"Fila {row_num}: se esperan 5 columnas, se encontraron {len(row)}")
                    continue

                col1, col2, col3, col4, col5 = row

                if not col1.isdigit() or not (3 <= len(col1) <= 10):
                    errors.append(f"Fila {row_num}, Columna 1: '{col1}' no es un entero válido de 3–10 dígitos")
                email_regex = r'^\S+@\S+\.\S+$'

                if not re.match(email_regex, col2):
                    errors.append(f"Fila {row_num}, Columna 2: '{col2}' no es un correo válido")

                if col3 not in ["CC", "TI"]:
                    errors.append(f"Fila {row_num}, Columna 3: '{col3}' debe ser CC o TI")

                try:
                    val = int(col4)
                    if not (500000 <= val <= 1500000):
                        errors.append(f"Fila {row_num}, Columna 4: '{col4}' fuera de rango (500000–1500000)")
                except:
                    errors.append(f"Fila {row_num}, Columna 4: '{col4}' no es un número")

            if not errors:
                success = True

    else:
        form = UploadFileForm()

    return render(request, "upload.html", {
        "form": form,
        "errors": errors,
        "success": success
    })
