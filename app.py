from datetime import datetime
import plotly.express as px
import streamlit as st
import funciones
import pytz
import LAS
import credenciales as cd


MES = "Septiembre"
chile_tz = pytz.timezone('America/Santiago')

dia_hoy = datetime.now(chile_tz).replace(hour=0, minute=0, second=0, microsecond=0)


def main(paginas):

    st.set_page_config("Control de Equipos", "img\\Logo IDEAL OSITO RGB.png", "wide", "collapsed")

    """Código fuente del panel interactivo"""
    pagina_seleccionada = st.sidebar.selectbox("Páginas", paginas)

    if pagina_seleccionada == "Página principal":
        funciones.pie_pagina(pagina_seleccionada, "Monitoreo en general de Control de Equipos")
        st.text('Instrucciones para el Llenado del "LAS"')
        st.image(r"img/Manual de movimientos LAS.png")

    elif pagina_seleccionada == "Despacho CEDIS":
        funciones.pie_pagina(
            pagina_seleccionada, 
            """Registro de bandejas despachadas desde el centro de distribución hasta 
            el centro de ventas, debes registrar todos los equipos despachados desde 
            el Centro de Distribución.""")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            datos_formulario, enviado = funciones.crear_formulario_cedis("Registro despacho ramplas")
            if enviado:
                st.success("Registro realizado")
                funciones.enviar_formulario(datos_formulario, "1ZImEypaWBpzAQN71ROnQnBd41dWbd63kLeDf6GJESu0")
        
        with col2:
            funciones.ultimos_registros_cedis()

    elif pagina_seleccionada == "Certificación Planta":
        funciones.pie_pagina(
            pagina_seleccionada,
            """Registro de equipos recibidos en planta, se debe cuantificar toda la cantidad de Equipos
            que retornen a Planta para que sean cosiderados en el programa""")
        
        col1, col2 = st.columns(2)

        with col1:
            datos_formulario, enviado = funciones.crear_formulario("Registro retorno ramplas")
            if enviado:
                st.success("Registro realizado")
                funciones.enviar_formulario(datos_formulario, "1_0UUt-WmP2Am_-AvbDXLr53EQ5aUn5qjNeBFdx6k63A")

        with col2:
            funciones.ultimos_registros_planta()


    elif pagina_seleccionada == "Reportes":

        funciones.pie_pagina(pagina_seleccionada, "Movimientos de retornos desde los centros de venta.")

        with st.spinner("Realizando descarga... espera unos minutos"):
            df_las = LAS.descargar_las(MES)
            df_lleagada = funciones.cruce_camiones(df_las)
            st.success("¡Descarga realizada con éxito!")

        st.write("Estado de Rampla")
        st.dataframe(df_lleagada)   

if __name__ == "__main__":

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        
        funciones.login_ideal()
    
    if st.session_state.authenticated:
        main(st.session_state.resultado)
