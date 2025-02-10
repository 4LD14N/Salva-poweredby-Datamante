import re
import pandas as pd

# Ruta de los archivos de entrada
BCP_FILE = './app/data/bcp_details.xlsx'
YAPE_FILE = './app/data/yape_details.xlsx'
YAPE_1_FILE = './app/data/yape_1_details.xlsx'

def normalize_fecha_hora(fecha_hora):
    
    if not isinstance(fecha_hora, str):
        return fecha_hora  # Devolver el valor original si no es una cadena
    
    # def convertir_fecha(fecha):
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12',
        'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'ago': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12', 
        'set': '09'
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
        r'(\d{1,2}) (\w+) (\d{4})(?:\s-?\s?(\d{1,2}:\d{2})(:\d{2})?\s?([APap]\.?\s?[Mm]\.?)?)?', #25 agosto 2024 - 06:57 p. m.
        r'(\d{2}) (\w+)\. (\d{4}) - (\d{1,2}:\d{2})(:\d{2})?\s?([APap]\.?[Mm]\.?)'  # 04 Ene. 2025 - 11:52 am
        ]
    
    replacements = [
        lambda m: f"{m.group(3)}-{m.group(2)}-{m.group(1)} {convert_to_24_hour(m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else ''))}",  # 10/12/2023 - 8:56 PM
        lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4) or '00:00:00'}",  # 2023-01-26 10:13:49
        lambda m: f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)} {m.group(4) or '00:00:00'}",  # 28/2/2024 - 21:56:10
        lambda m: f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)} {convert_to_24_hour(m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else ''))}",  # 01 de junio de 2024 - 01:54 PM
        lambda m: f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)} {convert_to_24_hour(m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else ''))}",  # Domingo, 01 Octubre 2023 - 12:20 P. M.
        lambda m: f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)} {convert_to_24_hour(m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else ''))}",  # 25 agosto 2024 - 06:57 p. m.
        lambda m: f"{m.group(3)}-{meses[m.group(2).lower()]}-{m.group(1).zfill(2)} {convert_to_24_hour(m.group(4) + (m.group(5) or ':00') + (' ' + m.group(6).replace('.', '').replace(' ', '').upper() if m.group(6) else ''))}"  # 04 Ene. 2025 - 11:52 am
    ]

    for i, patron in enumerate(regex):
        match = re.search(patron, fecha_hora)
        if match:
            return replacements[i](match)
    
    return '2000-01-01 00:00:00'  # Si no coincide con ningún patrón, devolver la fecha original
    
        
def extract_currency_and_amount(monto):
    """
    Extrae el tipo de moneda y el monto de una cadena con formato específico.

    Formatos soportados:
    - S/ 1,234.56
    - $ 123.45
    - 55.3 (asume S/ como moneda predeterminada)

    Retorna:
    - Tuple (tipo_moneda, monto) o (None, None) si el formato no coincide.
    """
    if not monto:  # Manejo explícito de valores vacíos o nulos
        return None, None
    
    # Convertir a cadena y eliminar espacios
    monto = str(monto).strip()
    
    # Patrón para detectar tipo de moneda y monto
    patron = re.match(r'(\$|S\/)?\s?([\d,]+\.\d{1,2})', monto)
    
    if patron:
        moneda = patron.group(1) if patron.group(1) else 'S/'  # Moneda predeterminada: S/
        cantidad = float(patron.group(2).replace(',', ''))
        # print("imprimiendo moneda y cantidad: " +moneda,cantidad)
        return moneda, cantidad

    return None, None

# Cargar el archivo Excel
df = pd.read_excel(BCP_FILE)
df2 = pd.read_excel(YAPE_FILE)
df3 = pd.read_excel(YAPE_1_FILE)

# Definir los patrones permitidos BCP
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

# print(df.head())
# print(df2.head())
# print(df3.head())

# Aplicar la función de normalización a la columna 'fecha_hora'
df['fecha_hora'] = df['fecha_hora'].apply(normalize_fecha_hora)
df2['fecha_hora'] = df2['fecha'].apply(normalize_fecha_hora)
df3['fecha_hora'] = df3['fecha_hora'].apply(normalize_fecha_hora)

# Crear nuevas columnas para el tipo de moneda y el monto
df['tipo_moneda'], df['monto'] = zip(*df['monto_total'].apply(extract_currency_and_amount))
df2['tipo_moneda'], df2['monto'] = zip(*df2['monto'].apply(extract_currency_and_amount))
df3['tipo_moneda'], df3['monto'] = zip(*df3['monto_total'].apply(extract_currency_and_amount))

# Asignar el valor 'yape' a una nueva columna 'tipo_operacion' en df2
df2['tipo_operacion'] = 'yape'
df3['tipo_operacion'] = 'yape_servicios'

# Crear la columna 'entidad' en df usando 'destino_nombre_titular' solo para los de 'tipo_operacion' igual a 'Constancia de transferencia a terceros' o 'Transferencia a terceros BCP'
df['entidad'] = df.apply(lambda row: row['destino_nombre_titular'] if row['tipo_operacion'] in ['Constancia de transferencia a terceros', 'Transferencia a terceros BCP', 'Transferencia a otros bancos', 'Transferencia a otro banco', 'Pago de tarjeta a tercero BCP', 'Pago de tarjeta propia BCP'] else row['empresa'], axis=1)

# Crear la nueva columna 'entidad' combinando 'empresa' y 'servicio'
df3['entidad'] = df3.apply(lambda row: f"{row['empresa']}, {row['servicio']}" if pd.notnull(row['empresa']) and pd.notnull(row['servicio']) else row['empresa'] or row['servicio'], axis=1)


# Crear un DataFrame base con las columnas necesarias
columnas_necesarias = [
    'id', 'nro_operacion', 'tipo_operacion', 'entidad', 'monto',
    'tipo_moneda', 'nro_tarjeta', 'compras_internet', 
    'compras_extranjero', 'dispocision_efectivo', 'fecha_hora'
]

# Seleccionar y renombrar columnas para cada DataFrame
df = df[['ID', 'numero_operacion', 'entidad', 'tipo_operacion', 'empresa', 'monto', 'tipo_moneda', 'origen_ultimos_digitos', 'compras_internet', 'compras_extranjero', 'dispocision_efectivo', 'fecha_hora']].rename(columns={
    'ID': 'id',
    'numero_operacion': 'nro_operacion',
    'origen_ultimos_digitos': 'nro_tarjeta'
})

df2 = df2[['id', 'operacion', 'beneficiario', 'monto', 'tipo_moneda', 'fecha_hora', 'tipo_operacion']].rename(columns={
    'operacion': 'nro_operacion',
    'beneficiario': 'entidad'
})

df3 = df3[['id', 'operacion_yape', 'monto', 'tipo_moneda', 'empresa', 'fecha_hora', 'tipo_operacion', 'entidad']].rename(columns={
    'operacion_yape': 'nro_operacion'
})

# Asegurar que todas las columnas necesarias están presentes
for df_tmp in [df, df2, df3]:
    for col in columnas_necesarias:
        if col not in df_tmp.columns:
            df_tmp[col] = None


# Concatenar los DataFrames
df_combinado = pd.concat([df, df2, df3], ignore_index=True)

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
    # Excluir registros con fecha "2000-01-01 00:00:00"
    if fila['fecha_hora'] == pd.Timestamp('2000-01-01 00:00:00'):
        continue

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
