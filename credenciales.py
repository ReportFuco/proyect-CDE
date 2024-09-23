import pandas as pd
import os

def credenciales(perfil: str, contraseña: str):

    rol = None

    file_path = os.getenv('EXCEL_FILE_PATH')
    df = pd.read_csv(file_path, sep=";")
    if perfil in df["Usuario_ID"].unique():
        validar = df[df["Usuario_ID"] == perfil].reset_index().loc[0, "Password"]
        if validar == contraseña:
            print("Acceso correcto")

            rol = df[df["Usuario_ID"] == perfil].reset_index().loc[0, "Rol"]
        else:
            print()
            return None, None, "usuario y contraseña incorrectos"
    else:
        print()
        return None, None, "usuario no se encuentra en la base de datos"


    accesos_rol = {
        "Administrador": ["Página principal", "Despacho CEDIS", "Certificación Planta", "Reportes"],
        "Despachador": ["Página principal", "Despacho CEDIS"],
        "Recibidor": ["Página principal", "Certificación Planta"]
    }

    return perfil, rol, accesos_rol[rol]