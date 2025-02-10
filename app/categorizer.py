import os
import pandas as pd
from langchain_ollama import OllamaLLM
import re

# Definir rutas de archivos
input_file = './app/data/datos_combinados_filtrados.xlsx'
output_file = './app/data/gastos_categorizados.xlsx'

# Verificar si el archivo categorizado existe
if os.path.exists(output_file):
    df = pd.read_excel(output_file)  # Cargar archivo categorizado existente
else:
    df = pd.read_excel(input_file)  # Cargar archivo original

# Asegurarse de que la columna 'categoría_by_llama3' exista
if 'categoría_by_llama3' not in df.columns:
    df['categoría_by_llama3'] = None

# Inicializar el modelo Llama3
llm = OllamaLLM(model="llama3.2", temperature=0)

# Función para categorizar una transacción
def categorize(expense):
    if pd.notnull(expense['categoría_by_llama3']) and expense['categoría_by_llama3'].strip():
        return expense['categoría_by_llama3']  # Si ya tiene categoría, conservarla

    entidad = str(expense['entidad']) if not pd.isnull(expense['entidad']) else ""
    parts = re.split(r'[\*\-]', entidad)
    prompt = ""
    response = ""

    # Reglas personalizadas según el tipo de operación
    if expense['tipo_operacion'] == "yape":
        response = "Billetera digital"
    elif "transferencia" in expense['tipo_operacion'].lower():
        response = "Transferencia"
    elif expense['tipo_operacion'] == "Retiro":
        response = "Efectivo"
    else:
        if "PLIN" in parts or "YAPE" in parts:
            response = "Billetera digital"
        elif "IZI" in parts:
            response = "Proveedor de pagos electrónicos"
        elif "" in parts:
            response = "Desconocido"
        elif "CE " in entidad:
            entidad_part = entidad.split("CE ")[1].strip()
            prompt = f'''
            Identifica el servicio o producto del siguiente extracto peruana.

            {entidad_part}
            
            Responde lo más corto posible, por ejemplo: restaurante, internet, telefonía, electricidad, universidad, streaming, etc.
            No uses los dos puntos seguidos(:)
            '''
            response = llm.invoke(prompt)
        else:
            prompt = f'''
            Identifica el servicio o producto del siguiente extracto.

            {expense['entidad']}

            Responde lo más corto posible, por ejemplo: restaurante, internet, telefonía, electricidad, universidad, streaming, etc.
            No uses los dos puntos seguidos(:)
            '''
            response = llm.invoke(prompt)
    
    # Limpiar la respuesta
    cleaned_response = response.strip().rstrip('.')
    print(f"Prompt enviado:\n{prompt}\nRespuesta recibida:\n{cleaned_response}")
    return cleaned_response if isinstance(cleaned_response, str) else ""


# Aplicar la función categorize solo en filas sin categoría
df.loc[df['categoría_by_llama3'].isnull() | df['categoría_by_llama3'].str.strip().eq(""), 'categoría_by_llama3'] = df.apply(categorize, axis=1)

# Guardar los datos categorizados en el archivo
df.to_excel(output_file, index=False)

print(f"Archivo categorizado guardado en: {output_file}")
