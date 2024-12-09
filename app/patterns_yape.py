import re

def dataExtract(text, id):
    text = text.replace('\n', ' ').strip()

    patterns = {
        # "REMITENTE": r"Hola, ([A-Z ]+)!",
        "MONTO": r"S/[\s]*([\d,]+\.\d{2})",
        "REMITENTE_CEL": r"Tu número de celular ([X\d]{9,})",
        "FECHA": r"Fecha y Hora de la operación (\d{1,2} \w+ \d{4} - \d{2}:\d{2} [ap]\. m\.)",
        "BENEFICIARIO_CEL": r"Celular del Beneficiario ([X\d]{9,})",
        #"BENEFICIARIO": r"Nombre del Beneficiario ([A-ZÁÉÍÓÚÑ \-\.]+) N[°º]",
        "BENEFICIARIO": r"(?i)Nombre del Beneficiario ([a-záéíóúñÁÉÍÓÚÑ \-\.]+) N[°º]",
        "OPERACION": r"N[°º] de operación (\d+)"
    }

    entities = {}
    
    for entity, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            entities[entity] = match.group(1)
    
    def getData(entities):
        yapeJson = {
            "id": id,
            # "remitente": entities.get("REMITENTE"),
            "beneficiario": entities.get("BENEFICIARIO"),
            "monto": float(entities.get("MONTO").replace(',', '')) if entities.get("MONTO") else None,
            "fecha": entities.get("FECHA"),
            "remitente_cel": entities.get("REMITENTE_CEL"),
            "beneficiario_cel": entities.get("BENEFICIARIO_CEL"),
            "operacion": entities.get("OPERACION"),
        }
        return yapeJson

    entitiesData = getData(entities)

    return entitiesData
