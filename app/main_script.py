import sys
import os
import pandas as pd
from datetime import datetime, timezone
from gmail_auth import gmail_authenticate
import get_mail
import patterns_yape
import patterns_bcp

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


def guardar_fecha(sender, date_path, current_utc_time):
    if os.path.exists(date_path):
        with open(date_path, 'r') as file:
            dates_data = eval(file.read())
    else:
        dates_data = {}

    dates_data[sender] = int(current_utc_time.timestamp())

    with open(date_path, 'w') as file:
        file.write(str(dates_data))


def obtener_fecha(sender, date_path):
    if os.path.exists(date_path):
        with open(date_path, 'r') as file:
            dates_data = eval(file.read())
            return dates_data.get(sender, "1672534800")
    return "1672534800"


def main():
    print("************* START *************\n")

    date_path = "./app/data/last_processed_date.txt"
    current_utc_time = datetime.now(timezone.utc)

    senders = [
        'notificaciones@notificacionesbcp.com.pe',
        'notificaciones@yape.pe',
        # 'notificaciones@notificacionesbcp.com.pe',
    ]

    count = 0
    service = gmail_authenticate()

    if service:
        for sender in senders:
            last_processed_date = obtener_fecha(sender, date_path)
            print(f"Última fecha procesada para {sender}: {last_processed_date}")

            ids = get_mail.getId(service, sender, last_processed_date)

            if ids:
                print(f"IDs obtenidos del Gmail para {sender}: {len(ids)} correos nuevos.")
                guardar_fecha(sender, date_path, current_utc_time)

                if sender == 'notificaciones@yape.pe':
                    data = {
                        'id': [],
                        'beneficiario': [],
                        'monto': [],
                        'fecha': [],
                        'remitente_cel': [],
                        'beneficiario_cel': [],
                        'operacion': []
                    }
                elif sender == 'notificaciones@notificacionesbcp.com.pe':
                    data = {
                        'ID': [],
                        'patron': [],
                        'tipo_operacion': [],
                        'fecha_hora': [],
                        'empresa': [],
                        'numero_operacion': [],
                        'canal': [],
                        'servicio': [],
                        'titular_servicio': [],
                        'cod_usuario': [],
                        'origen_tipo_cuenta': [],
                        'origen_ultimos_digitos': [],
                        'origen_nombre_titular': [],
                        'monto_total': [],
                        'vencimiento': [],
                        'importe': [],
                        'cargo_fijo': [],
                        'mora': [],
                        'compras_internet': [],
                        'compras_extranjero': [],
                        'dispocision_efectivo': [],
                        'cta_ahorro': [],
                        'fecha_emision': [],
                        'destino_tipo_cuenta': [],
                        'destino_ultimos_digitos': [],
                        'destino_nombre_titular': [],
                        'otros': []
                    }
                else:
                    print("Error: remitente no soportado")
                    continue

                print(f"Cabecera de los datos para {sender}: {data}")
                print("Extrayendo datos...\n")

                nro_text = 0
                for id in ids:
                    nro_text += 1
                    payload = get_mail.getPayload(service, id)
                    print(payload['mimeType'][1])
                    html = get_mail.getHtml(payload)
                    txt = get_mail.getTextMail(html)
                    print(nro_text, txt)

                    if sender == 'notificaciones@yape.pe':
                        json = patterns_yape.dataExtract(txt, id)
                    elif sender == 'notificaciones@notificacionesbcp.com.pe':
                        json = patterns_bcp.dataExtract(txt, id)
                    else:
                        print("Error al procesar el remitente")
                        continue

                    print(json)
                    print("\n")

                    for key, value in json.items():
                        if key in data:
                            data[key].append(value)

                    count += 1

                print(f"Correos procesados para {sender}: {count}")
                df = pd.DataFrame(data)

                if sender == 'notificaciones@yape.pe':
                    file_path = './app/data/yape_details.xlsx'
                elif sender == 'notificaciones@notificacionesbcp.com.pe':
                    file_path = './app/data/bcp_details.xlsx'

                if os.path.exists(file_path):
                    before_df = pd.read_excel(file_path)
                    new_df = pd.concat([before_df, df], ignore_index=True)
                else:
                    new_df = df

                new_df.to_excel(file_path, index=False)
                print(f"Archivo Excel creado para {sender}: {file_path}\n")
            else:
                print(f"No se encontraron correos nuevos para {sender}.\n")
    
   

        print("************* END *************")
    else:
        print("Error al autenticarse con Gmail")


if __name__ == "__main__":
    main()
