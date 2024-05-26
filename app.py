import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

from añadir_datos import obtener_datos

# Ejecutar la función obtener_datos para actualizar los datos y guardarlos en session_state
obtener_datos()

df_datos_completo = st.session_state['df_datos_completo']

# Excluir la columna de fecha y obtener los nombres de las columnas restantes
nombres_columnas = [col for col in df_datos_completo.columns if col != 'Fecha']

# Opción para seleccionar qué columna graficar
columna_seleccionada = st.sidebar.selectbox("Selecciona la columna para graficar:", nombres_columnas)

# Opciones de visualización
opciones_visualizacion = {
    'Todos los tiempos': df_datos_completo,
    'Últimos 30 días': df_datos_completo[df_datos_completo['Fecha'] >= datetime.now() - timedelta(days=30)],
    'Mes actual': df_datos_completo[df_datos_completo['Fecha'].dt.month == datetime.now().month],
    'Últimos 7 días': df_datos_completo[df_datos_completo['Fecha'] >= datetime.now() - timedelta(days=7)],
    'Día actual': df_datos_completo[df_datos_completo['Fecha'].dt.date == datetime.now().date()]
}
opcion_visualizacion = st.sidebar.selectbox("Selecciona la opción de visualización:", list(opciones_visualizacion.keys()))

# Obtener los datos para la opción seleccionada
datos_visualizacion = opciones_visualizacion[opcion_visualizacion]

# Crear la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Función para inicializar la animación
def init():
    ax.set_xlabel('Fecha')
    ax.set_ylabel(columna_seleccionada)
    ax.set_title(f'Gráfico de {columna_seleccionada} - {opcion_visualizacion}')
    ax.set_xlim(min(datos_visualizacion['Fecha']), max(datos_visualizacion['Fecha']))
    ax.set_ylim(0, max(datos_visualizacion[columna_seleccionada]) + 1)
    return line,

# Función para actualizar la animación en cada cuadro
def update(frame):
    datos = datos_visualizacion.iloc[:frame+1]
    line.set_data(datos['Fecha'], datos[columna_seleccionada])
    return line,

# Ejecutar la animación
ani = FuncAnimation(fig, update, frames=len(datos_visualizacion), init_func=init, blit=True)

# Guardar la animación como un archivo de video
video_file = "animation.mp4"
ani.save(video_file)

# Mostrar el video en Streamlit
video_bytes = open(video_file, "rb").read()
st.video(video_bytes)

# Descripción del proyecto
st.markdown("""
# Monitor de Mediciones
Este proyecto muestra la evolución de las mediciones en diferentes períodos de tiempo. 
Puedes seleccionar la columna de datos que deseas visualizar y el período de tiempo correspondiente.
""")
