import streamlit as st
import pandas as pd
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

# Crear la gráfica
st.title(f'Gráfico de {columna_seleccionada} - {opcion_visualizacion}')
fig, ax = plt.subplots()

# Verificar si la opción de visualización es para el día actual
if opcion_visualizacion == 'Día actual':
    # Ordenar los datos cronológicamente
    datos_visualizacion = datos_visualizacion.sort_values(by='Fecha')
    # Formatear la fecha para mostrar solo la hora
    datos_visualizacion['Hora'] = datos_visualizacion['Fecha'].dt.strftime('%H:%M')
    plt.plot(datos_visualizacion['Hora'], datos_visualizacion[columna_seleccionada], color='#33FFD1', marker='o')  # Modificación visual: Color personalizado y marcador
    plt.xlabel('Hora')  # Modificación visual: Etiqueta del eje X
    # Ajustar las etiquetas del eje X para mostrar solo cada hora
    x_ticks = datos_visualizacion['Hora'].iloc[::12]  # Cada 12*5 = 60 minutos = 1 hora
    plt.xticks(rotation=45, ha='right')  # Modificación visual: Rotación y alineación de las etiquetas del eje X
    plt.gca().set_xticks(x_ticks)  # Modificación visual: Establecer los ticks en el eje X
else:
    plt.plot(datos_visualizacion['Fecha'], datos_visualizacion[columna_seleccionada], color='#33FFD1', marker='o')  # Modificación visual: Color personalizado y marcador
    plt.xlabel('Fecha')  # Modificación visual: Etiqueta del eje X

plt.ylabel(columna_seleccionada)  # Modificación visual: Etiqueta del eje Y
plt.title(f'{columna_seleccionada} a lo largo de {opcion_visualizacion}', color='#33FFD1', fontsize=16, fontweight='bold')  # Modificación visual: Título personalizado
plt.yticks(color='#33FFD1')  # Modificación visual: Color de las etiquetas del eje Y
plt.gca().spines['top'].set_visible(False)  # Modificación visual: Ocultar borde superior del gráfico
plt.gca().spines['right'].set_visible(False)  # Modificación visual: Ocultar borde derecho del gráfico
plt.gca().tick_params(axis='both', colors='#33FFD1')  # Modificación visual: Color de los ticks en ambos ejes

plt.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Descripción del proyecto
st.markdown("""
# Monitor de Mediciones
Este proyecto muestra la evolución de las mediciones en diferentes períodos de tiempo. 
Puedes seleccionar la columna de datos que deseas visualizar y el período de tiempo correspondiente.
""")
