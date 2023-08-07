import requests
import json
import pandas as pd

def api_ssw(cnpj, nro_nf):
    senha = ""

    url = "https://ssw.inf.br/api/tracking"
    headers = {"Content-Type": "application/json"}
    payload = {
        "cnpj": cnpj,
        "senha": senha,
        "nro_nf": nro_nf
    }

    response = requests.post(url, headers=headers, json=payload)
    tracking_info = response.json()
    remetente = tracking_info['header']['remetente']
    destinatario = tracking_info['header']['destinatario']
    tracking = tracking_info['tracking']
    last_item = tracking[-1] if tracking else None
    
    data_hora = []
    cidade = []
    ocorrencia = []
    descricao = []
    tipo = []
    data_hora_efetiva = []
    nome_recebedor = []
    
    # All Items
    for item in tracking:
        data_hora.append(item['data_hora'])
        cidade.append(item['cidade'])
        ocorrencia.append(item['ocorrencia'])
        descricao.append(item['descricao'])
        tipo.append(item['tipo'])
        data_hora_efetiva.append(item['data_hora_efetiva'])
        nome_recebedor.append(item['nome_recebedor'])
    
    return (remetente, destinatario, data_hora, cidade, ocorrencia, descricao, tipo, data_hora_efetiva, nome_recebedor) 


    """
    # Last Item
    if last_item:
        data_hora = last_item['data_hora']
        cidade = last_item['cidade']
        ocorrencia = last_item['ocorrencia']
        descricao = last_item['descricao']
        tipo = last_item['tipo']
        data_hora_efetiva = last_item['data_hora_efetiva']
        nome_recebedor = last_item['nome_recebedor']
        tracking = tracking_info['tracking']
        print(tracking)
        return (remetente, destinatario, data_hora, cidade, ocorrencia, descricao, tipo, data_hora_efetiva, nome_recebedor, tracking) 
    """
    return None

cnpj = '18398145000158'
nro_nf = '37826'
api_ssw(cnpj, nro_nf)