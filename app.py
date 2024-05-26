import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import subprocess

# Usar seaborn para el estilo
sns.set(style="darkgrid")

# Ejecutar añadir_datos.py
subprocess.run(["python", "añadir_datos.py"])  # este .py añade los datos nuevos al CSV

# Cargar los datos desde el archivo CSV
file_path = "mediciones.csv"
data = pd.read_csv(file_path)

# Convertir la columna 'Fecha' a datetime
data['Fecha'] = pd.to_datetime(data['Fecha'])

# Excluir la columna de fecha y obtener los nombres de las columnas restantes
nombres_columnas = [col for col in data.columns if col != 'Fecha']

# Opción para seleccionar qué columna graficar
columna_seleccionada = st.sidebar.selectbox("Selecciona la columna para graficar:", nombres_columnas)

# Opciones de visualización
opciones_visualizacion = {
    'Todos los tiempos': data,
    'Últimos 30 días': data[data['Fecha'] >= datetime.now() - timedelta(days=30)],
    'Mes actual': data[data['Fecha'].dt.month == datetime.now().month],
    'Últimos 7 días': data[data['Fecha'] >= datetime.now() - timedelta(days=7)],
    'Día actual': data[data['Fecha'].dt.date == datetime.now().date()]
}
opcion_visualizacion = st.sidebar.selectbox("Selecciona la opción de visualización:", list(opciones_visualizacion.keys()))

# Obtener los datos para la opción seleccionada
datos_visualizacion = opciones_visualizacion[opcion_visualizacion]

# Crear la gráfica
st.title(f'Gráfico de {columna_seleccionada} - {opcion_visualizacion}')
fig, ax = plt.subplots()

# Verificar si la opción de visualización es para el día actual
if opcion_visualizacion == 'Día actual':
    datos_visualizacion = datos_visualizacion.sort_values(by='Fecha')
    datos_visualizacion['Hora'] = datos_visualizacion['Fecha'].dt.strftime('%H:%M')
    sns.lineplot(x='Hora', y=columna_seleccionada, data=datos_visualizacion, ax=ax)
    ax.set_xlabel('Hora')
    x_ticks = datos_visualizacion['Hora'].iloc[::12]
    ax.set_xticks(x_ticks)
else:
    sns.lineplot(x='Fecha', y=columna_seleccionada, data=datos_visualizacion, ax=ax)
    ax.set_xlabel('Fecha')
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Ajustar para mostrar máximo 10 etiquetas

ax.set_ylabel(columna_seleccionada)
ax.set_title(f'{columna_seleccionada} a lo largo de {opcion_visualizacion}')
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

st.markdown("""
# Monitor de Mediciones
Este proyecto muestra la evolución de las mediciones en diferentes períodos de tiempo. 
Puedes seleccionar la columna de datos que deseas visualizar y el período de tiempo correspondiente.
""")
