import pandas as pd
from langchain_ollama import OllamaLLM
import re

# Cargar los datos
df = pd.read_excel('./app/data/datos_combinados_filtrados.xlsx')

# Asegurarse de que la columna 'categoría_by_llama3' exista
if 'categoría_by_llama3' not in df.columns:
    df['categoría_by_llama3'] = None

# Inicializar el modelo Llama3
llm = OllamaLLM(model="llama3.2", temperature=0)

# Función para categorizar una transacción
def categorize(expense):
    # Si ya hay una categoría, no hacer nada
    if pd.notnull(expense['categoría_by_llama3']) and expense['categoría_by_llama3'].strip() != "":
        return expense['categoría_by_llama3']
    
    # Extraer la entidad de expense
    entidad = str(expense['entidad']) if not pd.isnull(expense['entidad']) else ""
    
    # Dividir usando '*' o '-' como delimitadores
    parts = re.split(r'[\*\-]', entidad)
    
    prompt = ""
    response = ""
    
    # Reglas personalizadas según el tipo de operación
    if expense['tipo_operacion'] == "yape":
        print("Es una transacción de YAPE.")
        response = "Billetera digital"
    elif "transferencia" in expense['tipo_operacion'].lower():
        print("Es una Transferencia")
        response = "Transferencia"
    elif expense['tipo_operacion'] == "Retiro":
        print("Es un retiro de efectivo.")
        response = "Efectivo"
    else:
        # Reglas adicionales
        if "PLIN" in parts or "YAPE" in parts:
            print("Es una transacción de PLIN o YAPE.")
            response = "Billetera digital"
        elif "IZI" in parts:
            print("Es una transacción de IZIPAY.")
            response = "Provedor de pagos electrónicos"
        elif "" in parts:
            print("Es una entidad gubernamental.")
            response = "None"
        elif "CE " in entidad:
            # Dividir la entidad por "CE " para tomar la segunda parte
            entidad_part = entidad.split("CE ")[1].strip()
            print("Es una entidad con CE adelante.")
            prompt = f'''
            Identifica el servicio o producto de la entidad peruana.

            {entidad_part}
    
            Responde lo más corto posible, por ejemplo: restaurante, internet, telefonía, electricidad, universidad, streaming, etc.
            No uses los dos puntos seguidos(:)
            '''
            response = llm.invoke(prompt)
        else:
            print("Entidad identificada por IA.")
            prompt = f'''
            Identifica el servicio o producto de la entidad.

            {expense['entidad']}
    
            Responde lo más corto posible, por ejemplo: restaurante, internet, telefonía, electricidad, universidad, streaming, etc.
            No uses los dos puntos seguidos(:)
            '''
            response = llm.invoke(prompt)
    
    # Limpiar la respuesta
    cleaned_response = response.strip().rstrip('.')
    
    print(f"Prompt enviado:\n{prompt}\nRespuesta recibida:\n{cleaned_response}")
    return cleaned_response.strip() if isinstance(cleaned_response, str) else ""

# Aplicar la función categorize si la categoría está vacía
df['categoría_by_llama3'] = df.apply(categorize, axis=1)

# Guardar los datos categorizados en un nuevo archivo
df.to_excel('./app/data/gastos_categorizados.xlsx', index=False)
