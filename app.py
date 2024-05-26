import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

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
st.title(f'Gráfico de {columna_seleccionada} - {opcion_visualizacion}')
fig, ax = plt.subplots()

# Verificar si la opción de visualización es para el día actual
if opcion_visualizacion == 'Día actual':
    # Ordenar los datos cronológicamente
    datos_visualizacion = datos_visualizacion.sort_values(by='Fecha')
    # Formatear la fecha para mostrar solo la hora
    datos_visualizacion['Hora'] = datos_visualizacion['Fecha'].dt.strftime('%H:%M')
    sns.lineplot(x='Hora', y=columna_seleccionada, data=datos_visualizacion, ax=ax)
    ax.set_xlabel('Hora')
    # Ajustar las etiquetas del eje X para mostrar solo cada hora
    x_ticks = datos_visualizacion['Hora'].iloc[::12]  # Cada 12*5 = 60 minutos = 1 hora
    ax.set_xticks(x_ticks)
else:
    # Implementación de visualización con colores cambiantes
    x = np.arange(len(datos_visualizacion))
    y = datos_visualizacion[columna_seleccionada]
    dydx = np.gradient(y)

    # Create a set of line segments
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(dydx.min(), dydx.max())
    cmap = plt.get_cmap('viridis')
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(dydx)
    lc.set_linewidth(2)
    ax.add_collection(lc)

ax.set_ylabel(columna_seleccionada)
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Descripción del proyecto
st.markdown("""
# Monitor de Mediciones
Este proyecto muestra la evolución de las mediciones en diferentes períodos de tiempo. 
Puedes seleccionar la columna de datos que deseas visualizar y el período de tiempo correspondiente.
""")
