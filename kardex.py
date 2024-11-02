from datetime import timedelta
from datetime import datetime as dt
from shareplum import Office365, Site
from shareplum.site import Version
from urllib.parse import unquote
from io import BytesIO
from config import *
import pandas as pd
import openpyxl


class ExtraccionKardex:
    """Clase para las conecciones con Kardex y LAS para
      extraer y subir archivos de Sharepoint"""
    
    def __init__(self, user, password):
        self.auth = Office365(
            SITE_GB, 
            username=user, 
            password=password).GetCookies()
        
        self.site_kardex = Site(
            site_url=SITE_DOWNLOAD_KARDEX, 
            version=Version.v365, 
            authcookie=self.auth)
        

    @staticmethod
    def dato_fecha():
        if dt.now().strftime('%A') == "Monday":
            return dt.now() - timedelta(days=2)
        else: 
            return dt.now() - timedelta(days=1)
        

    def descarga_archivo(self, carpeta_sharepoint, nombre_archivo):
        
        carpeta = self.site_kardex.Folder((f"Documentos%20compartidos/{carpeta_sharepoint}"))
        contenido_archivo = carpeta.get_file(nombre_archivo)
        
        return BytesIO(contenido_archivo)


    def extraer_kardex(self, carpeta, nombre_archivo, fecha_descarga):
        """Extrae la información de los archivos Kardex y cambia el formato"""
        
        libro_kardex = openpyxl.load_workbook(self.descarga_archivo(carpeta, nombre_archivo), data_only=True)
        active_sheet = libro_kardex[fecha_descarga.strftime("%d.%m")]
        max_row = active_sheet.max_row

        dic_kardex = {
            "AGENCIA": [a[0].value for a in active_sheet[f"A3:A{max_row}"]],
            "RUTA": [a[0].value for a in active_sheet[f"B3:B{max_row}"]],
            "CANAL": [a[0].value for a in active_sheet[f"C3:C{max_row}"]],
            "CARGA": [a[0].value for a in active_sheet[f"L3:L{max_row}"]],
            "DEVOLUCION": [a[0].value for a in active_sheet[f"AA3:AA{max_row}"]]
        }

        df = pd.DataFrame(dic_kardex)

        df.dropna(how="all", inplace=True)
        df["FECHA"] = fecha_descarga.strftime("%d-%m-%Y")

        df = df[["FECHA", "AGENCIA", "RUTA", "CANAL", "CARGA", "DEVOLUCION"]].reset_index(drop=True)

        return df

    def guardar_kardex(self, df, fecha):

        site = Site(SITE_UPLOAD_KARDEX, version=Version.v365, authcookie=self.auth)
        carpeta = site.Folder(FOLDER_UPLOAD)
        file_content = df.read()

        carpeta.upload_file(file_content, f"{fecha.strftime('%d.%m.%y')}.csv")

    def extraccion_kardex(self, mes_kardex, fecha_descarga):
        """Extracción del todos los Kardex a nivel nacional para transformarlos
        en un archivo CSV y mandarlo a sharepoint"""
        
        df = pd.DataFrame()
        for carpeta in SALES_CENTER(mes_kardex):

            for centro, archivo in SALES_CENTER(mes_kardex)[carpeta].items():

                df_extraccion = self.extraer_kardex(carpeta, archivo, fecha_descarga)
                df = pd.concat([df, df_extraccion], ignore_index=False)

        for serie in ["RUTA", "CARGA", "DEVOLUCION"]:
            try:
                df[serie] = df[serie].astype(int)
            except ValueError:
                import streamlit as st
                st.warning("Debes corregir Kardex, tiene un dato string")
                return df

        csv_ram = BytesIO()

        df.to_csv(csv_ram, index=False, sep=";", encoding="utf-8-sig")
        csv_ram.seek(0)
                
        self.guardar_kardex(df=csv_ram,fecha=fecha_descarga)

        return df