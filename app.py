import streamlit as st
from PIL import Image
import funciones
import LAS


MES = "Octubre"

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
            datos_formulario, enviado = funciones.crear_formulario("Registro retorno ramplas", rol)
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
        main(st.session_state.resultado, st.session_state.rol)