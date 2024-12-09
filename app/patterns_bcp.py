import re


def dataExtract(text,id):
    
    data = {
            'ID': id,
            'patron': None,
            # 'destinatario': None,
            'tipo_operacion': None,
            # 'tarjeta_credito': None,
            # 'tarjeta_debito': None,
            # 'cod_cajero': None,
            'fecha_hora': None,
            'empresa': None,
            'numero_operacion': None,
            # 'monto': None,
            'canal': None,
            # 'tarjeta_pagada': None,
            # 'tipo_pago': None,
            # 'cuenta_origen': None,
            # 'cuenta_destino': None,
            'servicio': None,
            'titular_servicio': None,
            'cod_usuario': None,
            'origen_tipo_cuenta': None,
            'origen_ultimos_digitos': None,
            'origen_nombre_titular': None,
            'monto_total': None,
            'vencimiento': None,
            'importe': None,
            'cargo_fijo': None,
            'mora': None,
            'compras_internet': None,
            'compras_extranjero': None,
            'dispocision_efectivo': None,
            'cta_ahorro': None,
            'fecha_emision': None,
            'destino_tipo_cuenta': None,
            'destino_ultimos_digitos': None,
            'destino_nombre_titular': None,
            'otros': None
        }
    
    # Definir los patrones para identificar el tipo de operación
    service_type = {
        "pago_servicios": r'Operación realizada: \*(.*?) de servicios\*', #patron de referencia
        "consumo": r'Realizaste un (consumo)', #patron de referencia
        "pago_tarjetas": r'Realizaste un pago de tarjeta |Realizaste un pago a tu tarjeta',
        "devolucion": r'te brindamos los detalles de la (devolución)',
        "rechazo": r'te brindamos los detalles de la (operación rechazada)',
        "configuracion": r'te enviamos los cambios que realizaste en tu Tarjeta (.*?)',
        "solicitud": r'Constancia de (solicitud)',
        # "transferencia": r'Realizaste una (transferencia)',
        "transferencia": r'\btransferencia\b',
        "app_organizate": r'(organizatebcp)',
        "afiliacion": r'Este es tu código de (validación)',
        "atencion": r'Ten presente que tu atención|Tienes una reserva próxima|agenda de cita',
        "anything": r'Sigamos transformando tus planes en (realidad)',
        "alerta": r'Muchas gracias por atender nuestra (alerta)',
        "operacion": r'Realizaste una (operación)',
        "favorito": r', Tu (favorito)',
        "retiro": r'Realizaste un (retiro)',
        "token": r'Token Digital'
    }
    
    # Verificar el tipo de operación
    tipo_operacion = None
    for tipo, patron in service_type.items():
        if re.search(patron, text):
            tipo_operacion = tipo
            break
        
    if not tipo_operacion:
        return {"error": "Tipo de operación no encontrado"}
    
    # Definir los patrones para extraer cada campo
    patrones_1 = { 
        # "patron": 'pago_servicios',
        "tipo_operacion": r'Operación realizada: \*(.*?)\*',
        "numero_operacion": r'Número de operación: \*(\d+)\*',
        "fecha_hora": r'Fecha y hora: \*(.*?)\*',
        "empresa": r'Empresa: \*(.*?)\*',
        "servicio": r'Servicio: \*(.*?)\*',
        "titular_servicio": r'Titular del servicio: \*(.*?)\*',
        "cod_usuario": r'Código de usuario: \*?([A-Za-z0-9]+)\*? ',
        "origen_tipo_cuenta": r'Cuenta de origen: \*(.*?)\*',
        "origen_ultimos_digitos": r'\*\*\*\* (\d{4})',
        "origen_nombre_titular": r'\*\*\*\* \d{4} (.*?)\*',            
        "monto_total": r'Monto total: \*(S/ \d+\.\d{2}|\$ \d+\.\d{2})\*',
        # "doc_pago": r'Doc. pago: \*(.*?)\*',
        "vencimiento": r'Vencimiento: \*(.*?)\*',
        "importe": r'Importe: \*(S/ \d+\.\d{2})\*',
        "cargo_fijo": r'Cargo fijo: \*(S/ \d+\.\d{2})\*',
        "mora": r'Mora: \*(S/ \d+\.\d{2})\*'
    }
    
    patrones_2 = {
        # "tipo_operación": r'Realizaste un (.*?) de',
        "monto_total": r'Realizaste un consumo de (S/ \d+\.\d{2}|\$ \d+\.\d{2})',  # Extraer el monto total del consumo
        # "tipo_operacion": r'Operación realizada (.*?) Fecha',  # Extraer el tipo de operación
        "tipo_operacion": r'Operación realizada (.*?)(?: Fecha| Monto)',
        "fecha_hora": r'Fecha y hora (\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2}|\d{2} de \w+ de \d{4} - \d{2}:\d{2}:\d{2}|\d{2} de \w+ de \d{4} \d{2}:\d{2}:\d{2})',  # Extraer la fecha y hora
        "origen_tipo_cuenta": r'Número de (.*?) \*',
        "origen_ultimos_digitos": r'\*\*\*\*(\d{4})', # Extraer el número de tarjeta de débito
        "empresa": r'Empresa (.*?) Número de operación',  # Extraer la empresa
        "numero_operacion": r'Número de operación (\d+)'  # Extraer el número de operación
    }
    
    pago_tarjetas = {
        "monto_total": r'Monto pagado \*?(S/ \d+\.\d{2}|\$ \d+\.\d{2})\*?',  # Extraer el monto total del consumo
        "tipo_operacion": r'Operación realizada \*?(.*?)\*? Fecha?',
        "fecha_hora": r'Fecha y hora \*?(\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2}|\d{2} de \w+ de \d{4} - \d{2}:\d{2}:\d{2}|\d{2} de \w+ de \d{4} \d{2}:\d{2}:\d{2}|\w+, \d{1,2} \w+ \d{4} - \d{2}:\d{2} [ap]\. m\.|\d{2}/\d{2}/\d{4} - \d{2}:\d{2} [APM]{2})',  # Extraer la fecha y hora
        "numero_operacion": r'Número de operación \*?(\d+)\*?',  # Extraer el número de operación
        "destino_tipo_cuenta": r'Pagado a (.*?)\*\*\*\* \d{4} (.*?) Desde\*',
        "destino_ultimos_digitos": r'\*\*\*\* (\d{4}) .*? Desde',
        "destino_nombre_titular": r'Pagado a \*?(.*?)\*',
        "origen_tipo_cuenta": r'(?:origen:|Desde) \*?(.*?)\*?',
        "origen_ultimos_digitos": r'Desde \*?.*? ?\*\*\*\* (\d{4})',
        "canal": r'Canal \*?(.*?)(?:\*|BCP)'
    }
    
    patron_retiro = {
        "tipo_operacion": r'Operación realizada (.*?)(?: Fecha| Monto)',
        "fecha_hora": r'Fecha y hora (\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2}|\d{2} de \w+ de \d{4} - \d{2}:\d{2}:\d{2}|\d{2} de \w+ de \d{4} \d{2}:\d{2}:\d{2}|\w+, \d{1,2} \w+ \d{4} - \d{2}:\d{2} [ap]\.m\.?|\d{2}/\d{2}/\d{4} - \d{2}:\d{2} [APM]{2})',  # Extraer la fecha y hora
        "numero_operacion": r'Número de operación (\d+)',  # Extraer el número de operación
        "origen_tipo_cuenta": r'Número de (.*?) \*',
        "origen_ultimos_digitos": r'\*\*\*\* ?(\d{4})',
        "monto_total": r'(?:Monto|retirado) (S/ \d+\.\d{2}|\$ \d+\.\d{2})',  # Extraer el monto total del consumo
        "canal": r'Canal \*?(.*?)\*? Código?'
        
    }
    
    
    patrones_3 = {
        "monto_total": r'Monto Total devuelto (S/ \d+\.\d{2})',  
        "tipo_operacion": r'te brindamos los detalles de la (devolución)',
        "fecha_hora": r'Fecha y hora (\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2})', 
        "destino_ultimos_digitos": r'\*\*\*\*(\d{4})', 
        "empresa": r'Nombre del Comercio (.*?) Número de operación', 
        "numero_operacion": r'Número de operación (\d+)'
    }
    
    patron_rechazo = {
        "monto_total": r'Importe de compra rechazada (S/ \d+\.\d{2}|\$ \d+\.\d{2})',  
        "tipo_operacion": r'Motivo de rechazo (.*?) Fecha',
        "fecha_hora": r'Fecha y hora (\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2})', 
        "origen_ultimos_digitos": r'\*\*\*\*(\d{4})', 
        "empresa": r'Nombre del Comercio (.*?) ¿'
    }
    
    patrones_4 = {
        "tipo_operacion": r'Operación realizada: \*(.*?)\*',
        "fecha_hora": r'Fecha y hora \*(.*?)\*', 
        "origen_ultimos_digitos": r'\*\*\*\*-(\d{4})', 
        "numero_operacion": r'Número de operación \*(\d+)\*',
        "compras_internet": r'Compras por internet \*(.*?)\*',
        "compras_extranjero": r'Compras en el extranjero \*(.*?)\*',
        "dispocision_efectivo": r'Disposición de efectivo \*(.*?)\*'
    }
    
    patrones_5 = {
        "tipo_operacion": r'Constancia de (.*?) -',
        "fecha_hora": r'Fecha y hora: (.*?) Número', 
        "origen_nombre_titular": r'BCP Titular: (.*?) Fecha',
        "origen_ultimos_digitos": r'\*\*\*\* (\d{4})', 
        "numero_operacion": r'Número de operación: (\d+) Estado',
        "cta_ahorro": r'Estado de cuenta: (.*?) Mes',
        "fecha_emision": r'Emisión: (.*?) Correo'
    }
    
    patron_transferencia = {
        "monto_total": r'(?:Monto transferido|Monto|Monto enviado)[:]? \*?(S/ [\d,]+\.\d{2}|\$ [\d,]+\.\d{2})',  
        # "tipo_operacion": r'Operación realizada (.*?) Fecha',
        "tipo_operacion": r'Operación realizada[:]? \*?(.*?)(?: Fecha|\*)',
        "fecha_hora": r'\*?(\d{2} de \w+ de \d{4} - \d{2}:\d{2} [APM]{2}|\d{2} de \w+ de \d{4} - \d{2}:\d{2}:\d{2}|\d{2} de \w+ de \d{4} \d{2}:\d{2}:\d{2}|\w+, \d{1,2} \w+ \d{4} - \d{2}:\d{2} [ap]\.m\.?|\d{2}/\d{2}/\d{4} - \d{1,2}:\d{2} [APM]{2})', 
        "destino_tipo_cuenta": r'(?:destino:|Enviado a) \*?(.*?) ?\*',
        # "destino_ultimos_digitos": r'Enviado a [^*]*\*+\s*(\d{4})|Enviado a \*[^*]*\* \*+ (\d{4})',
        "destino_ultimos_digitos": r'(?:Enviado a [^*]*\*+\s*|Enviado a \*[^*]*\* \*+ |destino: \*[^*]*\* \*+ )(\d{4})',
        # "destino_nombre_titular": r'(?:Cuenta de destino: (?!.*Cuenta de origen:)\D+ \d{4}\*|Enviado a) \*?(.*?) ?\*',
        # "destino_nombre_titular": r'(?:Cuenta de destino: \*?.*?\*\* \d{4}\*|Enviado a \*?.*?\*\* \d{4}\*) \*?(.*?) ?\*',
        "destino_nombre_titular": r'(?:Cuenta de destino: \*?.*?\*\* \d{4}\*|Enviado a) \*?(.*?) ?\*',
        "origen_tipo_cuenta": r'(?:origen:|Desde) \*?(.*?) ?\*',
        "origen_ultimos_digitos": r'(?:Desde|Cuenta de origen)[:]? .*? (\d{4})',
        "canal": r'Mensaje Canal (.*?) Número',
        "numero_operacion": r'Número de operación[:]? \*?(\d+)\*?'
    }
    
    patron_token = {
        "otros": r'Hola Cristhian, (.*?) ¿No reconoces'
    }
    
    patron_organizate = {
        "otros": r'\*Hola\* \*Cristhian Jorgi\* (.*?) \*Para dudas'
    }
    
    patron_afiliacion = {
        "otros": r'\*Hola REQUEJO SALVADOR CRISTHIAN JORGI,\* \*(.*?) ¿Necesitas'
    }
    
    patron_atencion = {
        # "otros": r'Hola (.*?) Ten presente|(¡Tienes una reserva .*?realizar.)'
        "otros": r'Hola (.*? Ten presente |.*? realizar.)'
    }
    
    patron_anything = {
        "otros": r'Hola (.*?) \*Sigamos transformando'
    }
    
    patron_alerta = {
        "fecha_hora": r'Fecha y hora de bloqueo \*(.*?)\*', 
        "origen_ultimos_digitos": r'\*\*\*\* (\d{4})',
        "canal": r'Canal \*(.*?)\*',
        "otros": r'Hola (.*?) Fecha y hora'
    }
    
    patron_operacion = {
        "monto_total": r'(?:Total de la operación|Monto|Total cobrado) (S/ \d+\.\d{2}|\$ \d+\.\d{2})',  
        # "tipo_operacion": r'Operación realizada (.*?) Fecha',
        "tipo_operacion": r'Operación realizada (.*?)(?: Monto| Fecha)',
        "fecha_hora": r'Fecha y hora (.*?) Número', 
        "origen_tipo_cuenta": r'con tu (.*?) BCP',
        "origen_ultimos_digitos": r'\*\*\*\*(\d{4})',
        "empresa": r'Empresa (.*?) Canal', 
        "canal": r'Canal de atención (.*?) Número',
        "numero_operacion": r'Número de operación (\d+)'
    }
    
    patron_favorito = {
        "otros": r'(Tu favorito .*?) Si deseas'
        
    }
    
    
    # Seleccionar el conjunto de patrones según el tipo de operación
    if tipo_operacion == "pago_servicios":
        patrones = patrones_1
    elif tipo_operacion == "consumo":
        patrones = patrones_2
    elif tipo_operacion == "pago_tarjetas":
        patrones = pago_tarjetas
    elif tipo_operacion == "retiro":
        patrones = patron_retiro
    elif tipo_operacion == "devolucion":
        patrones = patrones_3
    elif tipo_operacion == "rechazo":
        patrones = patron_rechazo
    elif tipo_operacion == "configuracion":
        patrones = patrones_4
    elif tipo_operacion == "solicitud":
        patrones = patrones_5
    elif tipo_operacion == "transferencia":
        patrones = patron_transferencia
    elif tipo_operacion == "token":
        patrones = patron_token    
    elif tipo_operacion == "app_organizate":
        patrones = patron_organizate
    elif tipo_operacion == "afiliacion":
        patrones = patron_afiliacion
    elif tipo_operacion == "atencion":
        patrones = patron_atencion
    elif tipo_operacion == "anything":
        patrones = patron_anything
    elif tipo_operacion == "alerta":
        patrones = patron_alerta
    elif tipo_operacion == "operacion":
        patrones = patron_operacion
    elif tipo_operacion == "favorito":
        patrones = patron_favorito
    else:
        patrones = {}
        
    # Asignar el tipo de patrón al diccionario data
    data['patron'] = tipo_operacion
    
    for clave, patron in patrones.items():
        coincidencia = re.search(patron, text)
        if coincidencia:
            data[clave] = coincidencia.group(1)
            
    
    return data
