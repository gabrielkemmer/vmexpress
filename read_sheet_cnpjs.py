import pandas as pd
import os
import requests
from app import *
import schedule
import time

def update_ocurrencies():
    client = MongoClient('mongodb+srv://gabrielkemmer:Fn741953.741953@microblog.ojr4lzw.mongodb.net/?retryWrites=true&w=majority')
    db = client['guilherme']
    consults_collection = db['consultas']


    actual_directory = os.getcwd()
    path = os.path.join(actual_directory, 'cnpjs/')
    cnpj_csv = path + 'cnpjs.xlsx'  # Specify the path to your PDF file

    df = pd.DataFrame(pd.read_excel(cnpj_csv))

    cnpjs = []
    notas = []

    for item in df["CNPJ REMETENTE"]:
        item = item.translate({ord('.'): None})
        item = item.translate({ord('/'): None})
        item = item.translate({ord('-'): None})
        cnpjs.append(item)

    for item in df["NFE"]:
        notas.append(item)

    tracking_infos = []
    url = "https://ssw.inf.br/api/tracking"
    headers = {"Content-Type": "application/json"}
    for cnpj, nota in zip(cnpjs, notas):
        payload = {
            "cnpj": cnpj,
            "senha": "",
            "nro_nf": nota
        }
        response = requests.post(url, headers=headers, json=payload)
        tracking_info = response.json()
        tracking_infos.append(tracking_info)

        for tracking_info in tracking_infos:
            remetente = tracking_info['header']['remetente']
            destinatario = tracking_info['header']['destinatario']
            tracking = tracking_info['tracking']

            occurrence_data = {
                'remetente': remetente,
                'destinatario': destinatario,
                'CNPJ': cnpj,
                'ocorrencias': []
            }

            for item in tracking:
                occurrence = {
                    'data_hora': item['data_hora'],
                    'cidade': item['cidade'],
                    'ocorrencia': item['ocorrencia'],
                    'descricao': item['descricao'],
                    'tipo': item['tipo'],
                    'data_hora_efetiva': item['data_hora_efetiva'],
                    'nome_recebedor': item['nome_recebedor']
                }
                occurrence_data['ocorrencias'].append(occurrence)

            check_nota = consults_collection.find_one({'nota': nota})

            if check_nota:
                # If the invoice exists, update the occurrence data by appending new occurrences
                consults_collection.update_one(
                            {'nota': nota},
                            {'$set': occurrence_data}
                        )
            else:
                # If the invoice doesn't exist, create a new document and insert occurrence data
                occurrence_data['nota'] = nota
                consults_collection.insert_one(occurrence_data)

schedule.every().day.at("01:00").do(update_ocurrencies)

while True:
    schedule.run_pending()
    time.sleep(1)