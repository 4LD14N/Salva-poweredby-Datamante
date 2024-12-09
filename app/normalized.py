import re
import pandas as pd

def normalize_fecha_hora(fecha_hora):
    
    if not isinstance(fecha_hora, str):
        return fecha_hora  # Devolver el valor original si no es una cadena
    
    # def convertir_fecha(fecha):
    meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }

    def convert_to_24_hour(hora_str):
            if 'AM' in hora_str or 'PM' in hora_str:
                hora_str = hora_str.strip()
                if 'AM' in hora_str:
                    periodo = 'AM'
                    hora_str = hora_str.replace('AM', '').strip()
                else:
                    periodo = 'PM'
                    hora_str = hora_str.replace('PM', '').strip()

                hora, minuto = map(int, hora_str.split(':')[:2])

                if periodo == 'PM' and hora != 12:
                    hora += 12
                elif periodo == 'AM' and hora == 12:
                    hora = 0

                return f"{hora:02}:{minuto:02}:00"
            return hora_str  # Si ya está en formato de 24 horas, simplemente devolverlo

    regex = [
            r'(\d{2})\/(\d{2})\/(\d{4})\s-\s(\d{1,2}:\d{2})(:\d{2})?\s([APap]\.?[Mm]\.?)',  #10/12/2023 - 8:56 PM
            r'(\d{4})-(\d{2})-(\d{2})(?:\s(\d{2}:\d{2}:\d{2}))?',  #2023-01-26 10:13:49
            r'(\d{1,2})/(\d{1,2})/(\d{4})(?:\s-?\s?(\d{2}:\d{2}:\d{2}))?', #28/2/2024 - 21:56:10
            r'(\d{1,2}) de (\w+) de (\d{4})(?:\s-?\s?(\d{1,2}:\d{2})(:\d{2})?\s?([APap]\.?[Mm]\.?)?)?', #01 de junio de 2024 - 01:54 PM
            r'\w+,\s?(\d{1,2})\s?(\w+)\s?(\d{4})(?:\s-?\s?(\d{1,2}:\d{2})(:\d{2})?\s?(AM|PM|[Aa]\.?\s?[Mm]\.?|[Pp]\.?\s?[Mm]\.?)?)?', #Domingo, 01 Octubre 2023 - 12:20 P. M.
            r'(\d{1,2}) (\w+) (\d{4})(?:\s-?\s?(\d{1,2}:\d{2})(:\d{2})?\s?([APap]\.?\s?[Mm]\.?)?)?' #25 agosto 2024 - 06:57 p. m.
        ]
    
    def replacement_type0(m): #10/12/2023 - 8:56 PM
            fecha = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            if m.group(4):
                hora = m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else '')
                fecha_hora = f" {convert_to_24_hour(hora)}"
                return fecha + fecha_hora
            else:
                return fecha

    def replacement_type1(m): #2023-01-26 10:13:49
            fecha = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            if m.group(4):
                hora = m.group(4)
                return fecha +" "+ hora
            else:
                return fecha

    def replacement_type2(m): #28/2/2024 - 21:56:10
            fecha = f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"
            if m.group(4):
                hora = m.group(4)
                return fecha +" "+ hora
            else:
                return fecha

    def replacement_type3(m): #01 de junio de 2024 - 01:54 PM
            # print(f"m.group(6): {m.group(6)}")
            fecha = f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)}"
            if m.group(4):
                hora = m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else '')
                fecha_hora = f" {convert_to_24_hour(hora)}"
                return fecha + fecha_hora
            else:
                return fecha

    def replacement_type4(m): #Domingo, 01 Octubre 2023 - 12:20 P. M.
            fecha = f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)}"
            if m.group(4):
                hora = m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else '')
                fecha_hora = f" {convert_to_24_hour(hora)}"
                return fecha + fecha_hora
            else:
                return fecha
            
    def replacement_type5(m): #25 agosto 2024 - 06:57 p. m.
            # print(f"m.group(6): {m.group(6)}")
            fecha = f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)}"
            if m.group(4):
                hora = m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else '')
                fecha_hora = f" {convert_to_24_hour(hora)}"
                return fecha + fecha_hora
            else:
                return fecha

    replacements = [replacement_type0, replacement_type1, replacement_type2, replacement_type3, replacement_type4, replacement_type5]
    
    
    for i, patron in enumerate(regex):
        match = re.search(patron, fecha_hora)
        if match:
            return replacements[i](match)
    
    return fecha_hora  # Si no coincide con ningún patrón, devolver la fecha original
    
        
def extract_currency_and_amount(monto):
    # Eliminar espacios en blanco
    monto = str(monto).strip()
    
    # Patrón para detectar el tipo de moneda y el monto
    patron = re.match(r'(\$|S/)\s?([\d,]+\.\d{2})', monto)
    
    if patron:
        moneda = patron.group(1)
        cantidad = float(patron.group(2).replace(',', ''))  # Eliminar comas y convertir a float
        
        # Devolver el tipo de moneda y el monto como un tuple
        return moneda, cantidad
    
    # Si no coincide con el patrón, devolver valores nulos (o manejarlo de otra manera)
    return None, None

# Cargar el archivo Excel
df = pd.read_excel('./app/data/bcp_details.xlsx')
df2 = pd.read_excel('./app/data/yape_details.xlsx')

# Definir los patrones permitidos
patrones_permitidos = [
    "configuracion", 
    "consumo", 
    # "devolucion", 
    "favorito", 
    "operacion", 
    "pago_servicios", 
    "pago_tarjetas", 
    # "rechazo", 
    "retiro",
    "transferencia"
]

# Filtrar df por los patrones permitidos
df = df[df['patron'].isin(patrones_permitidos)]

# Aplicar la función de normalización a la columna 'fecha_hora'
df['fecha_hora'] = df['fecha_hora'].apply(normalize_fecha_hora)
df2['fecha_hora'] = df2['fecha'].apply(normalize_fecha_hora)

# Crear nuevas columnas para el tipo de moneda y el monto
df['tipo_moneda'], df['monto'] = zip(*df['monto_total'].apply(extract_currency_and_amount))
df2['tipo_moneda'] = 'S/'

# Asignar el valor 'yape' a una nueva columna 'tipo_operacion' en df2
df2['tipo_operacion'] = 'yape'

# Crear diccionarios de mapeo para uniformar nombres de columnas
mapeo_df = {
    'ID': 'id',
    'numero_operacion': 'nro_operacion',
    'tipo_operacion': 'tipo_operacion',
    'empresa': 'entidad',
    'origen_ultimos_digitos': 'nro_tarjeta',
    'compras_internet': 'compras_internet',
    'compras_extranjero': 'compras_extranjero',
    'dispocision_efectivo': 'dispocision_efectivo'
}

mapeo_df2 = {
    'id': 'id',
    'operacion': 'nro_operacion',
    'beneficiario': 'entidad',
    'monto': 'monto',
}

# Renombrar columnas según el mapeo
df.rename(columns=mapeo_df, inplace=True)
df2.rename(columns=mapeo_df2, inplace=True)

columnas_necesarias = [
    'id', 'nro_operacion', 'tipo_operacion', 'entidad', 'monto',
    'tipo_moneda', 'nro_tarjeta', 'compras_internet', 
    'compras_extranjero', 'dispocision_efectivo', 'fecha_hora'
]
for col in columnas_necesarias:
    if col not in df.columns:
        df[col] = None
    if col not in df2.columns:
        df2[col] = None
        
# Concatenar los DataFrames
df_combinado = pd.concat([df, df2], ignore_index=True)

# Eliminar columnas completamente vacías
df_combinado = df_combinado.dropna(axis=1, how='all')

# Filtrar filas que tengan valores en 'nro_operacion'
df_combinado = df_combinado[df_combinado['nro_operacion'].notna()]

# Seleccionar solo las columnas necesarias
df_combinado_filtrado = df_combinado[columnas_necesarias].copy()

# Convertir la columna 'nro_operacion' a string utilizando loc[]
# df_combinado_filtrado['nro_operacion'] = df_combinado_filtrado['nro_operacion'].astype(str)
df_combinado_filtrado['nro_operacion'] = df_combinado_filtrado['nro_operacion'].astype(str).str.split('.').str[0]

# Asegurar que la columna 'fecha_hora' esté en formato datetime utilizando loc[]
df_combinado_filtrado['fecha_hora'] = pd.to_datetime(df_combinado_filtrado['fecha_hora'])

# Crear una nueva columna 'dia_semana' con el nombre del día de la semana
df_combinado_filtrado['dia_semana'] = df_combinado_filtrado['fecha_hora'].dt.day_name()

# Crear un diccionario para almacenar el registro más reciente para cada número de operación
registros_unicos = {}

# Función para decidir si un número es similar a uno ya visto
def es_similar(nro_actual, nro_visto):
    return nro_actual == nro_visto or nro_actual in nro_visto or nro_visto in nro_actual

# Procesar los registros y quedarse con el más reciente en caso de duplicados
for _, fila in df_combinado_filtrado.iterrows():
    nro_operacion_actual = fila['nro_operacion']
    if nro_operacion_actual in registros_unicos:
        # Comparar fechas y quedarse con el registro más reciente
        if fila['fecha_hora'] > registros_unicos[nro_operacion_actual]['fecha_hora']:
            registros_unicos[nro_operacion_actual] = fila
    else:
        # Verificar si hay un número similar ya registrado
        similar_encontrado = False
        for nro_visto in list(registros_unicos.keys()):
            if es_similar(nro_operacion_actual, nro_visto):
                similar_encontrado = True
                # Comparar fechas y quedarse con el registro más reciente
                if fila['fecha_hora'] > registros_unicos[nro_visto]['fecha_hora']:
                    registros_unicos[nro_visto] = fila
                break
        
        if not similar_encontrado:
            registros_unicos[nro_operacion_actual] = fila

# Convertir el diccionario de registros únicos de vuelta a un DataFrame
df_combinado_filtrado = pd.DataFrame(registros_unicos.values())



# Guardar el DataFrame filtrado en un nuevo archivo Excel
df_combinado_filtrado.to_excel('./app/data/datos_combinados_filtrados.xlsx', index=False)

# Imprimir las primeras filas para verificar los cambios
print(df_combinado_filtrado.head())
