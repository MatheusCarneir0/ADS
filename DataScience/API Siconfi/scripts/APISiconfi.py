import requests
import pandas as pd
import os
import time

BASE_URL = "http://apidatalake.tesouro.gov.br/ords/siconfi/"

def get_entes_federativos():
    url = f"{BASE_URL}tt/entes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Erro ao obter entes federativos: {response.status_code}")
        return []

def get_periodos_disponiveis():
    return [1, 2, 3, 4, 5, 6]

def download_anexos(ente, ano, periodo, tipo_relatorio):
    url = f"{BASE_URL}tt/{tipo_relatorio}?ente={ente}&ano={ano}&periodo={periodo}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()['items']
        
        # Salvar em CSV
        df = pd.DataFrame(dados)
        os.makedirs(f"dados/{tipo_relatorio}/{ano}/{periodo}", exist_ok=True)
        df.to_csv(f"dados/{tipo_relatorio}/{ano}/{periodo}/{ente}.csv", index=False)
        time.sleep(1)
    else:
        print(f"Erro ao baixar dados para {ente} - {ano}/{periodo}: {response.status_code}")

def main():
    entes = get_entes_federativos()
    anos = range(2014, 2025)  # Ajuste conforme os anos disponíveis
    periodos = get_periodos_disponiveis()
    for ente in entes:
        for ano in anos:
            for periodo in periodos:
                download_anexos(ente['ente'], ano, periodo, 'rreo')
                download_anexos(ente['ente'], ano, periodo, 'rgf')

if __name__ == "__main__":
    main()
