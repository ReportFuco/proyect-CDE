import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2 import service_account
import json
import os
import gspread
import re


def validar_patente(patente):
    """Validar que la patente cumpla con el formato xx-xx-xx"""
    patron = r"^[A-Za-z0-9]{2}-[A-Za-z0-9]{2}-[A-Za-z0-9]{2}$"
    if re.match(patron, patente):
        return True
    else:
        return False
    

def pie_pagina(titulo_pag: str, descripcion_pag):
    col1, col2, col3 = st.columns([1, 5, 2])

    with col1:
        st.image(r"img\Logo IDEAL OSITO RGB.png", use_column_width=True)

    with col2:
        st.title(titulo_pag)
        st.write(descripcion_pag, )
    with col3:
        st.write(f"Últ. actualización: {datetime.now().strftime("%d-%m-%y %H:%M")}")
    
    st.divider()


def crear_formulario(nombre_formulario: str):
    """Genera formulario para el registro de los movimientos LAS"""

    agencias = ['Selecciona una Agencia', 'ANTOFAGASTA', 'ARICA', 'CALAMA', 'CHILLAN', 'CONCEPCION', 
                'COPIAPO', 'GRANDES CLIENTES', 'IQUIQUE', 'LO ESPEJO', 'LOS ANDES', 
                'LOS ANGELES', 'MELIPILLA', 'OSORNO', 'PINAR', 'PUERTO MONTT', 
                'QUILICURA', 'RANCAGUA', 'SAN FERNANDO', 'SERENA', 'TALCA', 'TEMUCO', 'VALDIVIA', 'VIÑA']

    st.subheader("Certificación Rampla")

    with st.form(nombre_formulario, clear_on_submit=True):
        fecha_registro = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ceve_origen = st.selectbox("Centro de ventas", agencias)
        destino = st.selectbox("Planta destino", ["Selecciona una Planta", "PLANTA QUILICURA", "PLANTA CHILLÁN"]) 
        conequip = st.number_input("Conequip", min_value=0, max_value=99999999, step=1, format="%d")
        patente_rampla = st.text_input("Patente de Rampla [XX-XX-XX]")

        # Crear dos columnas
        col1, col2 = st.columns(2)

        # Inputs en la primera columna (Sin devolución)
        with col1:
            st.markdown("#### Equipo vacío")
            bg = st.number_input("Bandeja grande vacía", min_value=0, max_value=9999, step=1, format="%d")
            bme_sin_dev = st.number_input("Bandeja mediana vacía", min_value=0, max_value=9999, step=1, format="%d")
            bch_sin_dev = st.number_input("Bandeja chica vacía", min_value=0, max_value=9999, step=1, format="%d")
            pm_sin_dev = st.number_input("Pallet madera vacío", min_value=0, max_value=9999, step=1, format="%d")
            pn_sin_dev = st.number_input("Pallet negro vacío", min_value=0, max_value=9999, step=1, format="%d")
            pa_sin_dev = st.number_input("Pallet azul vacío", min_value=0, max_value=9999, step=1, format="%d")

        # Inputs en la segunda columna (Con devolución)
        with col2:
            st.markdown("#### Devolución")
            bg_con_dev = st.number_input("Bandeja grande con devolución", min_value=0, max_value=9999)
            bme_con_dev = st.number_input("Bandeja mediana con devolución", min_value=0, max_value=9999)
            bch_con_dev = st.number_input("Bandeja chica con devolución", min_value=0, max_value=9999)
            pm_con_dev = st.number_input("Pallet madera con devolución", min_value=0, max_value=9999)
            pn_con_dev = st.number_input("Pallet negro con devolución", min_value=0, max_value=9999)
            pa_con_dev = st.number_input("Pallet azul con devolución", min_value=0, max_value=9999)

        # Botón de envío del formulario
        boton_enviar = st.form_submit_button("Enviar registro")

    if boton_enviar:

        if ceve_origen == "Selecciona una Agencia":
            st.error("Debes elegir una Agencia")

        elif destino == "Selecciona una Planta":
            st.error("Debes elegir una planta")

        elif not validar_patente(patente_rampla):
            st.error("Formato incorrecto para la patente. Debe seguir el formato xx-xx-xx.")

        elif conequip == 0:
            st.error("Debes agregar el conequip")
        else:
            # Si todo está correcto, devolver los datos
            return [fecha_registro, ceve_origen, destino, conequip, patente_rampla.upper(), 
                    bg, bme_sin_dev, bch_sin_dev, pm_sin_dev, pn_sin_dev, pa_sin_dev, 
                    bg_con_dev, bme_con_dev, bch_con_dev, pm_con_dev, pn_con_dev, pa_con_dev], boton_enviar
    return None, None


def crear_formulario_cedis(nombre_formulario: str):
    """Genera formulario para el registro de los movimientos LAS"""

    agencias = ['Selecciona una Agencia', 'ANTOFAGASTA', 'ARICA', 'CALAMA', 'CHILLAN', 'CONCEPCION', 
                'COPIAPO', 'GRANDES CLIENTES', 'IQUIQUE', 'LO ESPEJO', 'LOS ANDES', 
                'LOS ANGELES', 'MELIPILLA', 'OSORNO', 'PINAR', 'PUERTO MONTT', 
                'QUILICURA', 'RANCAGUA', 'SAN FERNANDO', 'SERENA', 'TALCA', 'TEMUCO', 'VALDIVIA', 'VIÑA']

    st.subheader("Certificación Rampla")

    with st.form(nombre_formulario, clear_on_submit=True):

        fecha_registro = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ceve = st.selectbox("Centro de ventas", agencias)
        conequip = st.number_input("Conequip", min_value=0, max_value=9999999, step=1, format="%d")
        patente_rampla = st.text_input("Patente de Rampla [XX-XX-XX]")    
       
        st.markdown("#### Equipos enviados")
        bg = st.number_input("Bandeja grande", min_value=0, max_value=9999, step=1, format="%d")
        bme = st.number_input("Bandeja mediana", min_value=0, max_value=9999, step=1, format="%d")
        bch = st.number_input("Bandeja chica", min_value=0, max_value=9999, step=1, format="%d")
        pm = st.number_input("Pallet madera", min_value=0, max_value=9999, step=1, format="%d")
        pn = st.number_input("Pallet negro", min_value=0, max_value=9999, step=1, format="%d")
        pa = st.number_input("Pallet azul", min_value=0, max_value=9999, step=1, format="%d")

        # Botón de envío del formulario
        boton_enviar = st.form_submit_button("Enviar registro")

    if boton_enviar:

        if ceve == "Selecciona una Agencia":
            st.error("Debes elegir una Agencia")
        elif not validar_patente(patente_rampla):
            st.error("Formato incorrecto para la patente. Debe seguir el formato xx-xx-xx.")
        elif conequip == 0:
            st.error("Debes agregar el conequip")
        else:
            # Si todo está correcto, devolver los datos
            return [fecha_registro, ceve, conequip, patente_rampla.upper(), 
                    bg, bme, bch, pm, pn, pa], boton_enviar
    return None, None


def conexion_sheet_google(id):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    
    # Obtener las credenciales desde las variables de entorno
    credentials_info = os.getenv('GOOGLE_CREDENTIALS')
    
    # Convertir la cadena JSON en un diccionario de Python
    credentials_dict = json.loads(credentials_info)
    
    # Crear las credenciales desde el diccionario en lugar de un archivo
    credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    
    # Autorizar con las credenciales y acceder a Google Sheets
    client = gspread.authorize(credentials)
    spreadsheet_id = id
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1
    return worksheet


def enviar_formulario(datos, id):
    worksheet = conexion_sheet_google(id)
    worksheet.append_row(datos)


def ultimos_registros_planta():
    """Información de las bandejas certificadas en Planta"""

    st.subheader("Últimas certificaciones")
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1_0UUt-WmP2Am_-AvbDXLr53EQ5aUn5qjNeBFdx6k63A/export?format=csv")
    df["bandejas devolución"] = df["BG con devolución"] + df["BME con devolución"] + df["BCH con devolución"]
    df["Bandejas vacías"] = df["BG sin devolución"] + df["BME sin devolución"] + df["BCH sin devolución"]
    
    df = df.sort_values(by="Fecha", ascending=False)

    return st.dataframe(df[["Fecha", "Destino", "Agencia", "Bandejas vacías", "bandejas devolución"]], height=910)


def ultimos_registros_cedis():
    """Información de las bandejas certificadas en CEDIS"""

    st.subheader("Últimas certificaciones")
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1ZImEypaWBpzAQN71ROnQnBd41dWbd63kLeDf6GJESu0/export?format=csv")
    df["Total Bandejas"] = df["Bandeja Grande"] + df["Bandeja Mediana"] + df["Bandeja Chica"]

    df = df.sort_values(by="Fecha", ascending=False)

    return st.dataframe(df[["Fecha", "Agencia", "Total Bandejas"]], height= 890)


def ultimos_tres_dias():
    """Retorna los últimos 4 días para considerar"""
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return hoy - timedelta(4)

def cruce_camiones(dataframe_las):
    """Cruce de camiones entre el tránsito"""

    df_planta = pd.read_csv("https://docs.google.com/spreadsheets/d/1_0UUt-WmP2Am_-AvbDXLr53EQ5aUn5qjNeBFdx6k63A/export?format=csv")
    df_planta["Estado"] = "RECIBIDO"

    df = pd.merge(dataframe_las, df_planta, "outer", "Conequip")
    df.rename(columns={
        "Fecha_x":"Fecha despacho Agencia",
        "Fecha_y": "Fecha llegada",
        "Agencia_x": "Agencia",
        "Total Bandejas": "Bandejas enviadas"
        }, inplace=True)
    
    df.fillna({
        "Estado": "TRÁNSITO",
        "Destino": "POR DEFINIR",
        "Fecha llegada": "TRÁNSITO",
        "Bandejas enviadas": 0,
        "Agencia": "SIN REGISTRO CEVE",
        "Fecha despacho Agencia": "SIN REGISTRO CEVE"
    }, inplace=True)

    df["Total certificado"] = df["BG sin devolución"] + df["BME sin devolución"] + df["BCH sin devolución"] + df["BG con devolución"] + df["BME con devolución"] + df["BCH con devolución"]
    df["Total certificado"].fillna(0, inplace=True)


    return df[["Conequip", "Agencia", "Fecha despacho Agencia", "Fecha llegada", "Bandejas enviadas", "Total certificado", "Destino", "Estado"]].reset_index(drop=True)
