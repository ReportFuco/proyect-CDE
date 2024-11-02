from datetime import datetime, timedelta
import streamlit as st
from PIL import Image
from config import *
import funciones
import kardex as kd
import LAS


def main(paginas, rol):
    """Código fuente del panel interactivo"""
    st.set_page_config("Control de Equipos", "img/Logo IDEAL OSITO RGB.png", "wide", "collapsed")
    pagina_seleccionada = st.sidebar.selectbox("Páginas", paginas)

    if pagina_seleccionada == "Página principal":
        funciones.pie_pagina(pagina_seleccionada, "Monitoreo en general de Control de Equipos")
        st.write(f"intrucciones de uso: {rol}")
        if rol == "Despachador":
            img = Image.open(r"img/despacho_cedis.png")
            st.image(img.resize((img.width // 2, img.height // 2)))
        elif rol == "Recibidor":
            img = Image.open(r"img/certificacion_planta.png")
            st.image(img.resize((img.width // 2, img.height // 2)))
        elif rol == "Recibidor chillán":
            print("Yapo Erika apurese con las fotitos")

    elif pagina_seleccionada == "Despacho CEDIS":

        funciones.pie_pagina(
            pagina_seleccionada, 
            """Registro de bandejas despachadas desde el centro de distribución hasta 
            el centro de ventas, debes registrar todos los equipos despachados desde 
            el Centro de Distribución.""")
        
        col1, col2 = st.columns(2)
        
        with col1:
            datos_formulario, enviado = funciones.crear_formulario_cedis("Registro despacho ramplas", rol)
            if enviado:
                st.success("Registro realizado")
                funciones.enviar_formulario(datos_formulario, FORMS_CEDIS)
        with col2:
            funciones.ultimos_registros_cedis()

    elif pagina_seleccionada == "Certificación Planta":

        funciones.pie_pagina(
            pagina_seleccionada,
            """Registro de equipos recibidos en planta, se debe cuantificar toda la cantidad de Equipos
            que retornen a Planta para que sean cosiderados en el programa""")
        
        col1, col2 = st.columns(2)

        with col1:
            datos_formulario, enviado = funciones.crear_formulario("Registro retorno ramplas", rol)
            if enviado:
                st.success("Registro realizado")
                funciones.enviar_formulario(datos_formulario, FORMS_PLANTA)
        with col2:
            funciones.ultimos_registros_planta()

    elif pagina_seleccionada == "Reportes":
        funciones.pie_pagina(pagina_seleccionada, "Movimientos de retornos desde los centros de venta.")
        with st.spinner("Realizando descarga... espera unos minutos"):
            df_las = LAS.descargar_las(MONTH)
            df_lleagada = funciones.cruce_camiones(df_las)

        col1, col2, col3, col4 = st.columns(4)    

        with col1:
            filtro_estado = st.selectbox("Estado rampla", ["Todas"] + df_lleagada["Estado"].unique().tolist())
        with col2:
            filtro_agencia = st.selectbox("Agencia", ["Todas"] + df_lleagada["Agencia"].unique().tolist())
        with col3:
            filtro_fecha = st.selectbox("Fecha envío", ["Todas"] + df_lleagada["Fecha despacho Agencia"].unique().tolist())


        df_filtrado = df_lleagada.copy()

        if filtro_estado != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]
        if filtro_agencia != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Agencia"] == filtro_agencia]
        if filtro_fecha != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Fecha despacho Agencia"] == filtro_fecha]

        st.dataframe(df_filtrado)
    
    elif pagina_seleccionada == "Kardex":
        funciones.pie_pagina(pagina_seleccionada, "Movimientos del Kardex, puedes actualizar todos los dias dentro del Kardex")

        fecha_seleccionada = st.date_input(
            "Selecciona una fecha",
            datetime.now().date() - timedelta(1))
        
        if st.button("Extraer Kardex"):
            with st.spinner("Debes esperar la descarga del Kardex"):
                df_kardex = kd.ExtraccionKardex(
                    user=st.secrets["Shareplum"]["user"],
                    password=st.secrets["Shareplum"]["password"]
                ).extraccion_kardex(MONTH, fecha_seleccionada)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.dataframe(df_kardex)
                with col2:
                    st.dataframe(df_kardex.groupby("AGENCIA")[["CARGA", "DEVOLUCION"]].sum())
                with col3:
                    st.write(f"""
                    Fecha: {fecha_seleccionada}\n
                    Bandejas despachadas: {df_kardex["CARGA"].sum()}.\n
                    Bandejas Retornadas: {df_kardex["DEVOLUCION"].sum()}.\n
                    """)
        
if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        funciones.login_ideal()
    if st.session_state.authenticated:
        main(st.session_state.resultado, st.session_state.rol)