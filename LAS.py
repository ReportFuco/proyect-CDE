import pandas as pd
from shareplum import Office365, Site
from shareplum.site import Version
import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl as xlsx
from urllib.parse import unquote

@st.cache_data(ttl=600, show_spinner=False)
def descargar_las(mes):
    
    authcookie = Office365(
            'https://gbconnect.sharepoint.com/',
            username=st.secrets["Shareplum"]["user"],
            password=st.secrets["Shareplum"]["password"]
            ).GetCookies()

    site_mov_kardex = Site(
            "https://gbconnect.sharepoint.com/sites/KardexNacional905/",
            version= Version.v365,
            authcookie=authcookie    
    )

    centros_de_venta = {

        "Punto%20Centro%20Sur": {
            "Lo Espejo": f"Kardex%20Lo%20Espejo%20({mes}).xlsx",
            "Pinar": f"Kardex%20Pinar%20({mes}).xlsx",
            "Melipilla": f"Kardex%20Melipilla%20({mes}).xlsx",
            "Rancagua": f"Kardex%20Rancagua%20({mes}).xlsx",
            "San Fernando": f"Kardex%20San%20fernando%20({mes}).xlsx"
        },
        "Punto%20Centro%20Costa": {
            "Los Andes": f"Kardex%20Los%20andes%20({mes}).xlsx",
            "Quilicura": f"Kardex%20Quilicura%20({mes}).xlsx",
            "Grandes Clientes": f"Kardex%20Grandes%20Clientes%20({mes}).xlsx",
            "Viña del Mar": f"Kardex%20Vi%C3%B1a%20({mes}).xlsx"
        },
        "Punto%20Sur": {
            "Chillan": f"Kardex%20Chillan%20({mes}).xlsx",
            "Concepción": f"Kardex%20Concepcion%20({mes}).xlsx",
            "Los Ángeles": f"Kardex%20Los%20angeles%20({mes}).xlsx",
            "Osorno": f"Kardex%20Osorno%20({mes}).xlsx",
            "Puerto Montt": f"Kardex%20Puerto%20montt%20({mes}).xlsx",
            "Talca": f"Kardex%20Talca%20({mes}).xlsx",
            "Temuco": f"Kardex%20Temuco%20({mes}).xlsx",
            "Valdivia": f"Kardex%20Valdivia%20({mes}).xlsx"
        },
        "Punto%20Norte": {
            "Antofagasta": f"Kardex%20Antofagasta%20({mes}).xlsx",
            "Arica": f"Kardex%20Arica%20({mes}).xlsx",
            "Calama": f"Kardex%20Calama%20({mes}).xlsx",
            "Copiapó": f"Kardex%20Copiapo%20({mes}).xlsx",
            "Iquique": f"Kardex%20Iquique%20({mes}).xlsx",
            "Serena": f"Kardex%20Serena%20({mes}).xlsx"
        }
    }

    def extraer_archivo(carpeta, archivo):
        carpeta = site_mov_kardex.Folder(f"Documentos%20compartidos/{carpeta}")
        archivo = carpeta.get_file(archivo)
        return BytesIO(archivo)

    def extraer_las(archivo, nombre_archivo):
        kardex = xlsx.load_workbook(archivo, data_only=True)
        sheet_las = kardex["LAS"]
        max_row = 2000

        datos_las = sheet_las[f"K7:X{max_row}"]
        
        dic_las ={
            "Fecha": [data[0].value for data in datos_las],
            "Conequip" : [data[1].value for data in datos_las],
            "BG SIN DEV": [data[2].value for data in datos_las],
            "BME SIN DEV": [data[3].value for data in datos_las],
            "BCH SIN DEV": [data[4].value for data in datos_las],
            
            "P. MADERA SIN DEV": [data[5].value for data in datos_las],
            "P. NEGRO SIN DEV": [data[6].value for data in datos_las],
            "P. AZUL SIN DEV": [data[7].value for data in datos_las],
            
            "BG CON DEV": [data[8].value for data in datos_las],
            "BME CON DEV": [data[9].value for data in datos_las],
            "BCH CON DEV": [data[10].value for data in datos_las],
            
            "P. MADERA CON DEV": [data[11].value for data in datos_las],
            "P. NEGRO CON DEV": [data[12].value for data in datos_las],
            "P. AZUL CON DEV": [data[13].value for data in datos_las],
        } 

        df = pd.DataFrame(dic_las)
        df.dropna(how="all", inplace=True)
        pd.set_option('future.no_silent_downcasting', True)
        df.fillna({a:(0 if "CONEQUIP" in a else 0) for a in df.columns}, inplace=True)
        df["Agencia"] = unquote(nombre_archivo).replace(f" ({mes}).xlsx", "").replace("Kardex ", "").upper()

        try:    
            for columna in df.columns[3:15]:
                df[columna] = df[columna].astype(int)
        except ValueError as error:
            index = 0
            valor_error = df[df[columna].apply(lambda x: isinstance(x, str))].reset_index()
            print(f"\nTienes {len(valor_error[columna])} errores en {columna.title()}\n")
            for error in valor_error:
                print(f" - Debes arreglar el dato '{error}' de la agencia {valor_error['Agencia'].loc[0].title()}")
                print(f" - Número de ruta: {valor_error}")
                index += 1        

        df["Total vacías"] = df["BG SIN DEV"] + df["BME SIN DEV"] + df["BCH SIN DEV"]
        df["Total devolución"] = df["BG CON DEV"] + df["BME CON DEV"] + df["BCH CON DEV"]
        df["Total Bandejas"] = df["Total vacías"] + df["Total devolución"]

        return df

    df = pd.DataFrame()

    for carpeta in centros_de_venta.keys():
        for centro, archivo in centros_de_venta[carpeta].items():
            data = extraer_archivo(carpeta, archivo)
            df_agencia = extraer_las(data, archivo)
            df = pd.concat([df, df_agencia], ignore_index=True)

    df = df[["Fecha","Conequip","Agencia", "Total vacías", "Total devolución", "Total Bandejas"]]

    return df.sort_values(by="Fecha", ascending=False)
    