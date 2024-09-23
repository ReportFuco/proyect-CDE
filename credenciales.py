import streamlit as st
import pandas as pd
import os

def credenciales(perfil: str, contraseña: str):

    rol = None

    if perfil in st.secrets["Credencials"]:
        datos_usuario = st.secrets["Credencials"][perfil]

        if datos_usuario["password"] == contraseña:

            rol = datos_usuario["rol"]
        else:
            return None, None, "usuario y contraseña incorrectos"
    else:
        return None, None, "usuario no se encuentra en la base de datos"

    accesos_rol = {
        "Administrador": ["Página principal", "Despacho CEDIS", "Certificación Planta", "Reportes"],
        "Despachador": ["Página principal", "Despacho CEDIS"],
        "Recibidor": ["Página principal", "Certificación Planta"]
    }

    return perfil, rol, accesos_rol.get(rol, [])