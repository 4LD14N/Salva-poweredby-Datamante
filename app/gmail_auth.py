import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    """
    Función que realiza la autenticación con la API de Gmail.
    Returns:
        service: Un objeto de servicio de la API de Gmail.
    """
    creds = None
    # Revisa si hay credenciales almacenadas
    if os.path.exists("app/token.pickle"):
        with open("app/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, solicita al usuario que se autentique
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('app/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error durante la autenticación: {e}")
                return None
    # Guarda las credenciales para la próxima ejecución
    with open("app/token.pickle", "wb") as token:
        pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)
