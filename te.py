import streamlit as st
import pandas as pd

# Cargar datos
file_path = "Flujo de decisiones.xlsx"
df_conditions = pd.read_excel(file_path, sheet_name='Hoja1')  # Condiciones de evaluación
df_questions = pd.read_excel(file_path, sheet_name='Hoja2')   # Preguntas del formulario

# Asegurar que no haya espacios extra en los nombres de las columnas
df_conditions.rename(columns=lambda x: x.strip(), inplace=True)

# Título del formulario
st.title("Formulario tipo de Evaluación")

# Opción vacía
opcion_vacia = "Seleccionar"

# Selección múltiple para el destino
destinos = st.multiselect("1️⃣ Indique destino", df_questions['Indique destino'].dropna().unique())

# Determinar cantidad de destinos automáticamente
cantidad_destinos = len(destinos) if destinos else 0
st.markdown(f"<p style='font-size: 12px;'>Cantidad de destinos seleccionados: {cantidad_destinos}</p>", unsafe_allow_html=True)

# Otros filtros con numeración
libre_disponibilidad = st.selectbox("2️⃣ Desea Libre disponibilidad adicional", [opcion_vacia] + list(df_questions['Desea Libre disponibilidad adicional'].dropna().unique()))
compra_deuda = st.selectbox("3️⃣ Se comprará deuda con garantía hipotecaria", [opcion_vacia] + list(df_questions['Se comprará deuda con garantía hipotecaria de inversionista privado'].dropna().unique()))

# Cambiar número a texto para que aparezca vacío inicialmente
monto = st.text_input("4️⃣ Indique monto (en soles)", placeholder="Ingrese el monto")
plazo = st.text_input("5️⃣ Indique plazo (en meses)", placeholder="Ingrese el plazo")
edad = st.text_input("6️⃣ Indique edad", placeholder="Ingrese la edad")

sustento_ingresos = st.selectbox("7️⃣ Tiene sustentos de ingresos", [opcion_vacia] + list(df_questions['Tiene sustentos de ingresos'].dropna().unique()))
calificacion = st.selectbox("8️⃣ Peor calificación últimos 5 años", [opcion_vacia] + list(df_questions['PEOR CALIFICACIÓN'].dropna().unique()))
propiedad_garante = st.selectbox("9️⃣ Propiedad de garante", [opcion_vacia] + list(df_questions['Propiedad de garante'].dropna().unique()))
zonas_opciones = df_questions['Zonas admitidas'].dropna().unique().tolist()
if not zonas_opciones:  # Si la lista está vacía, agregar solo la opción vacía
    zonas_opciones = [opcion_vacia]

distrito = st.selectbox("🔟 Zonas admitidas", [opcion_vacia] + zonas_opciones)

# Filtrar datos progresivamente
filtered_df = df_conditions.copy()
columna_faltante = None  # Para capturar la primera columna que falte

try:
    if destinos and 'Indique destino' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Indique destino'].apply(lambda x: any(dest.strip() in [d.strip() for d in str(x).split(',')] for dest in destinos))]
    elif destinos:
        columna_faltante = 'Indique destino'

    if cantidad_destinos > 0 and 'Cantidad de destinos' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Cantidad de destinos'].apply(lambda x: any(str(cantidad_destinos) in str(val) for val in str(x).split(',')))]
    elif cantidad_destinos > 0:
        columna_faltante = 'Cantidad de destinos'

    if libre_disponibilidad != opcion_vacia and 'Desea Libre disponibilidad adicional' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Desea Libre disponibilidad adicional'].str.contains(libre_disponibilidad, na=False)]
    elif libre_disponibilidad != opcion_vacia:
        columna_faltante = 'Desea Libre disponibilidad adicional'

    if compra_deuda != opcion_vacia and 'Se comprará deuda con garantía hipotecaria de inversionista privado' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Se comprará deuda con garantía hipotecaria de inversionista privado'].str.contains(compra_deuda, na=False)]
    elif compra_deuda != opcion_vacia:
        columna_faltante = 'Se comprará deuda con garantía hipotecaria de inversionista privado'

    if monto.isdigit() and int(monto) > 0 and 'Indique monto' in filtered_df.columns:
        def is_in_range(value, monto):
            try:
                ranges = str(value).split('-')
                if len(ranges) == 2:
                    i, j = map(int, ranges)
                    return i <= monto <= j
                return False
            except:
                return False
        filtered_df = filtered_df[filtered_df['Indique monto'].apply(lambda x: is_in_range(x, int(monto)))]
    elif monto.isdigit() and int(monto) > 0:
        columna_faltante = 'Indique monto'

    if plazo.isdigit() and int(plazo) > 0 and 'Indique plazo' in filtered_df.columns:
        filtered_df = filtered_df[pd.to_numeric(filtered_df['Indique plazo'], errors='coerce') >= int(plazo)]
    elif plazo.isdigit() and int(plazo) > 0:
        columna_faltante = 'Indique plazo'

    if edad.isdigit() and int(edad) > 0 and 'Indique edad' in filtered_df.columns:
        def is_age_in_range(value, edad):
            try:
                ranges = str(value).split('-')
                if len(ranges) == 2:
                    i, j = map(int, ranges)
                    return i <= edad <= j
                return False
            except:
                return False
        filtered_df = filtered_df[filtered_df['Indique edad'].apply(lambda x: is_age_in_range(x, int(edad)))]
    elif edad.isdigit() and int(edad) > 0:
        columna_faltante = 'Indique edad'

    if sustento_ingresos != opcion_vacia and 'Tiene sustentos de ingresos' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Tiene sustentos de ingresos'].str.contains(sustento_ingresos, na=False)]
    elif sustento_ingresos != opcion_vacia:
        columna_faltante = 'Tiene sustentos de ingresos'

    if calificacion != opcion_vacia and 'PEOR CALIFICACIÓN' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['PEOR CALIFICACIÓN'].apply(lambda x: any(calificacion in str(val) for val in str(x).split(',')))]
    elif calificacion != opcion_vacia:
        columna_faltante = 'PEOR CALIFICACIÓN'

    if propiedad_garante != opcion_vacia and 'Propiedad de garante' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Propiedad de garante'].apply(lambda x: any(propiedad_garante in str(val) for val in str(x).split(',')))]
    elif propiedad_garante != opcion_vacia:
        columna_faltante = 'Propiedad de garante'

    if distrito != opcion_vacia and 'Zonas admitidas' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Zonas admitidas'].apply(lambda x: any(distrito in str(val) for val in str(x).split(',')))]
    elif distrito != opcion_vacia:
        columna_faltante = 'Zonas admitidas'

except KeyError as e:
    st.error(f"Error en el filtrado: columna {str(e)} no encontrada. Se omite el filtro correspondiente.")

# Verificar si el DataFrame filtrado tiene datos antes de acceder a la columna
if not filtered_df.empty and 'Tipo de evaluación viable' in filtered_df.columns:
    tipo_evaluacion = filtered_df['Tipo de evaluación viable'].unique()
else:
    tipo_evaluacion = []

st.subheader("Resultado de la Evaluación")
if len(tipo_evaluacion) > 0:
    for evaluacion in tipo_evaluacion:
        st.markdown(f"- {evaluacion}")  # Muestra cada evaluación en una lista con viñetas
else:
    if columna_faltante:
        st.write(f"No es gestionable")
    else:
        st.write("No es gestionable")
















