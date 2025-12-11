import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ministerio_educacion.settings")
django.setup()

from django.contrib.auth.models import User

CSV_FILE = "usuarios_aplicadores.csv"   # Cambialo si tu archivo se llama distinto

def importar_usuarios():
    # utf-8-sig elimina el BOM (\ufeff) automáticamente
    with open(CSV_FILE, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')

        print("Columnas detectadas:", reader.fieldnames)

        for row in reader:
            username = row["Cueanexo"]
            password = row["CUIL"]

            if User.objects.filter(username=username).exists():
                print(f"Usuario {username} ya existe. Saltando.")
                continue

            User.objects.create_user(
                username=username,
                password=password
            )

            print(f"Usuario creado: {username}")

    print("\nImportación completada.")


if __name__ == "__main__":
    importar_usuarios()
