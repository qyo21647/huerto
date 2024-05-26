import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# Crear un diccionario de colores para asociar cada tipo de medición con un color específico
colores = {
    'Temperatura': 'red',
    'Humedad': 'blue',
    'Intensidad de la luz': 'green',
    'Presión': 'orange',
    'Dirección del viento': 'purple',
    'Velocidad del viento': 'cyan',
    'Lluvia a la hora': 'brown',
    'Índice UV': 'magenta'
}

# Crear la gráfica
st.title(f'Gráfico de {columna_seleccionada} - {opcion_visualizacion}')
fig, ax = plt.subplots()

# Verificar si la opción de visualización es para el día actual
if opcion_visualizacion == 'Día actual':
    datos_visualizacion = datos_visualizacion.sort_values(by='Fecha')
    datos_visualizacion['Hora'] = datos_visualizacion['Fecha'].dt.strftime('%H:%M')
    for col in nombres_columnas:
        sns.lineplot(x='Hora', y=col, data=datos_visualizacion, ax=ax, color=colores[col], label=col)
    ax.set_xlabel('Hora')
    x_ticks = datos_visualizacion['Hora'].iloc[::12]
    ax.set_xticks(x_ticks)
else:
    for col in nombres_columnas:
        sns.lineplot(x='Fecha', y=col, data=datos_visualizacion, ax=ax, color=colores[col], label=col)
    ax.set_xlabel('Fecha')
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Ajustar para mostrar máximo 10 etiquetas

ax.set_ylabel(columna_seleccionada)
ax.set_title(f'{columna_seleccionada} a lo largo de {opcion_visualizacion}')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()  # Agregar leyenda

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Descripción del proyecto
st.markdown("""
# Monitor de Mediciones
Este proyecto muestra la evolución de las mediciones en diferentes períodos de tiempo. 
Puedes seleccionar la columna de datos que deseas visualizar y el período de tiempo correspondiente.
""")
