import re

def dataExtract(text, id):
    text = text.replace('\n', ' ').strip()

    # Diccionario de patrones para diferentes textos
    patterns = {
        "MONTO_TOTAL": r"(S/[\s]*[\d,]+\.\d{2})",
        "YAPERO": r"Yapero\(a\): ([A-ZÁÉÍÓÚÑ \-\.]+) N",
        "NUMERO_ASOCIADO": r"Número (?:de celular|asociado|de yapero): (\*{3} \*{3} \d+) F",
        "FECHA_HORA": r"(?:Fecha y hora|Fecha): (\d{1,2} \w+\.? \d{4} - \d{2}:\d{2} [apm]{2}|\d{2}\/\d{2}\/\d{4} a las \d{1,2}:\d{2}|\d{1,2} \w+\.? \d{4} - \d{2}:\d{2} [ap]\. m\.?)",
        "OPERACION_YAPE": r"N[°º] de operación Yape: (\d+)",
        "EMPRESA": r"Empresa: (.*) Servicio:",
        "SERVICIO": r"Servicio: (.*) Código",
        "CODIGO_USUARIO": r"Código de usuario: (\d+)",
        "TITULAR_SERVICIO": r"Titular del servicio: ([A-ZÁÉÍÓÚÑa-záéíóúñ\s\*\-\.]+) (?:Número|N[°º])",
        "NRO_DOCUMENTO": r"(?:N[°º] documento de pago|Número de recibo): (.*) Vencimiento",
        # "MONTO_PAGADO": r"Monto pagado: S/[\s]*([\d,]+\.\d{2})",
        # "RECARGA_EFECTIVA": r"Recarga Efectiva : S/[\s]*([\d,]+\.\d{2})",
        # "RUC": r"RUC: (\d+)"
    }

    entities = {}

    # Buscar coincidencias para cada patrón
    for entity, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            entities[entity] = match.group(1)

    # Convertir entidades extraídas a un diccionario estructurado
    def getData(entities):
        operationData = {
            "id": id,
            "monto_total": entities.get("MONTO_TOTAL"),
            # "monto_total": float(entities.get("MONTO_TOTAL", "0").replace(',', '')) if entities.get("MONTO_TOTAL") else None,
            "yapero": entities.get("YAPERO"),
            "numero_asociado": entities.get("NUMERO_ASOCIADO"),
            "fecha_hora": entities.get("FECHA_HORA"),
            "operacion_yape": entities.get("OPERACION_YAPE"),
            "empresa": entities.get("EMPRESA"),
            "servicio": entities.get("SERVICIO"),
            "codigo_usuario": entities.get("CODIGO_USUARIO"),
            "titular_servicio": entities.get("TITULAR_SERVICIO"),
            "nro_documento": entities.get("NRO_DOCUMENTO")
            # "monto_pagado": float(entities.get("MONTO_PAGADO", "0").replace(',', '')) if entities.get("MONTO_PAGADO") else None,
            # "recarga_efectiva": float(entities.get("RECARGA_EFECTIVA", "0").replace(',', '')) if entities.get("RECARGA_EFECTIVA") else None,
            # "ruc": entities.get("RUC")
        }
        return operationData

    entitiesData = getData(entities)
    return entitiesData

