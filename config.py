# Sites
SITE_GB = 'https://gbconnect.sharepoint.com/'
SITE_UPLOAD_KARDEX = "https://gbconnect.sharepoint.com/sites/MovimientosKardex/"
SITE_DOWNLOAD_KARDEX = 'https://gbconnect.sharepoint.com/sites/KardexNacional905/'

# Folder
FOLDER_UPLOAD = "Documentos%20compartidos/General/movimientos"

# Configuración mes
MONTH = "Octubre"

# Google API´s
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

#Forms Google
FORMS_PLANTA = "1_0UUt-WmP2Am_-AvbDXLr53EQ5aUn5qjNeBFdx6k63A"
FORMS_CEDIS = "1ZImEypaWBpzAQN71ROnQnBd41dWbd63kLeDf6GJESu0"


# Dataframes
DATAFRAME_PLANTA = "https://docs.google.com/spreadsheets/d/1_0UUt-WmP2Am_-AvbDXLr53EQ5aUn5qjNeBFdx6k63A/export?format=csv"
DATAFRAME_CEDIS = "https://docs.google.com/spreadsheets/d/1ZImEypaWBpzAQN71ROnQnBd41dWbd63kLeDf6GJESu0/export?format=csv"

# Agencias
def SALES_CENTER(mes): 
    return {

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