from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
# from datetime import datetime

# remitente = 'notificaciones@yape.pe'

def getId(service, remitente, last_processed_date):
    IDs = []
    nextPageToken = ""
    try:    
        while True:
            query = f"from:{remitente}"
            if last_processed_date:
                # last_processed_date  = "2024-05-23T19:37:10.195353"
                # date_obj = datetime.strptime(last_processed_date, "%Y-%m-%dT%H:%M:%S.%f")
                # epoch_time = int(date_obj.timestamp())
                query += f" after:{last_processed_date}"
        # print(query)

            results = service.users().messages().list(userId='me', labelIds=['INBOX'], q = query, pageToken=nextPageToken) .execute()
            messages = results.get('messages', [])

            for message in messages:
                IDs.append(message['id'])

            if 'nextPageToken' in results:
                nextPageToken = results['nextPageToken']
                # print('nextPageToken={}'.format(nextPageToken))
            else:
                break  

    except HttpError as e:
        print(f"An error occurred: {e}")
    
    #if last_processed_date == "1672534800":    
    #    with open("file.txt", 'w') as output:
    #        for row in IDs:
    #            output.write(str(row) + '\n')
    #else:
    #    with open("file.txt", 'a') as output:
    #        for row in IDs:
    #            output.write(str(row) + '\n')
                
    print("\n")
    return IDs 

def getPayload(service, msgID):
    msgObj = service.users().messages().get(userId="me", id=msgID).execute()
    payloadMail = msgObj['payload']
    return payloadMail

def getHtml(payloadMail):
    # print(payloadMail['mimeType'][1])
    
    if payloadMail['mimeType'] == 'multipart/alternative':
        secondPart = payloadMail['parts'][0]['body']['data']    
    elif payloadMail['mimeType'] == 'multipart/mixed':
        try:
            secondPart = payloadMail['parts'][0]['parts'][0]['body']['data']
        except Exception:
            secondPart = payloadMail['parts'][0]['body']['data']
    
    elif payloadMail['mimeType'] == 'text/html':
        secondPart = payloadMail['body']['data']
    else:
        return "Error obteniendo html del correo"
    return base64.urlsafe_b64decode(secondPart).decode('utf-8')

#############################################################################

def getTextMail(partsPayload):
    soup = BeautifulSoup(partsPayload, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print(text)
    textfinal = text.replace('\n', ' ').strip()
    return textfinal



