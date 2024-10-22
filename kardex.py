from datetime import timedelta
from datetime import datetime as dt
from shareplum import Office365, Site
from shareplum.site import Version
from urllib.parse import unquote
from io import BytesIO
import pandas as pd
import openpyxl


class ExtraccionKardex:
    """Clase para las conecciones con Kardex y LAS para
      extraer y subir archivos de Sharepoint"""
    
    def _init_(self, user, password, site):
        self.auth = Office365(
            'https://gbconnect.sharepoint.com/', 
            username=user, 
            password=password).GetCookies()
        
        self.site_kardex = Site(
            site_url=site, 
            version=Version.v365, 
            authcookie=self.auth)
        

    @staticmethod
    def dato_fecha():
        if dt.now().strftime('%A') == "Monday":
            return dt.now() - timedelta(days=2)
        else: 
            return dt.now() - timedelta(days=1)
        
    
    def elegir_dia(self):
        while True:
            dia_elegido = input("¿Extraer día anterior? [S/N]: ").upper()
            if dia_elegido == "S":
                return self.dato_fecha()
            
            elif dia_elegido == "N":
                return dt.strptime(input("Elige un día [dd-mm-yyyy]: "), "%d-%m-%Y")


    def descarga_archivo(self, carpeta_sharepoint, nombre_archivo):
        
        carpeta = self.site.Folder((f"Documentos%20compartidos/{carpeta_sharepoint}"))
        contenido_archivo = carpeta.get_file(nombre_archivo)
        
        return BytesIO(contenido_archivo)


    def extraer_kardex(self, carpeta, nombre_archivo):
        """Extrae la información de los archivos Kardex y cambia el formato"""
        
        libro_kardex = openpyxl.load_workbook(self.descarga_archivo(carpeta, nombre_archivo), data_only=True)
        active_sheet = libro_kardex[self.elegir_dia().strftime("%d.%m")]
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
        df["FECHA"] = self.elegir_dia().strftime("%d-%m-%Y")
        
        csv_ram = BytesIO()

        df = df[["FECHA", "AGENCIA", "RUTA", "CANAL", "CARGA", "DEVOLUCION"]].reset_index(drop=True)
        df.to_csv(csv_ram, index=False, sep=";", encoding="utf-8-sig")
        csv_ram.seek(0)

        self.guardar_kardex(csv_ram)

        return df

    def guardar_kardex(self, df):
        
        site = Site("https://gbconnect.sharepoint.com/sites/MovimientosKardex/", version=Version.v365, authcookie=self.auth)
        carpeta = site.Folder("Documentos%20compartidos/General/movimientos")
        file_content = df.read()

        carpeta.upload_file(file_content, f"{self.dato_fecha().strftime('%d.%m.%y')}.csv")

    def extraccion_kardex():

        pass