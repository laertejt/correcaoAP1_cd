import pandas as pd
import requests
import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")
headers = {'Authorization': 'JWT {}'.format(token)}
import logging
logger = logging.getLogger(__name__)


def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (defau

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]

def consultar_planilhao(data_base:date) -> list:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    dados (list): lista com o dicionario com todas as Ações.
    """
    params = {'data_base': data_base}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
        dados = r.json()['dados']
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return dados
    except Exception as e:
        logger.error(f"Erro na funcao consultar_planilhao: {e}")
        print(f"Erro na funcao consultar_planilhao: {e}")
    

def pegar_df_preco_corrigido(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período das ações da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        params = {'ticker':ticker, 'data_ini':data_ini, 'data_fim':data_fim }
        try:
            r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
            dados = r.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')        
        except Exception as e:
            logger.error(f"Erro na funcao pegar_df_preco_corrigido: {e}")
            print(f"Erro na funcao pegar_df_preco_corrigido: {e}")
    return df_preco

def pegar_df_preco_diversos(ticker:str, data_ini:date, data_fim:date) -> list:
    """
    Consulta os preços históricos de um ativo

    params:
    ticker (str): codigo do ativo a ser consultado
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta

    return:
    dados (list): lista com o dicionário com os preços diário histórico
    """
    params = {'ticker':ticker, 'data_ini':data_ini, 'data_fim':data_fim }
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos',params=params, headers=headers)
        dados = r.json()['dados']
        logger.info(f"Dados do Preco Diversos consultados com sucesso: {ticker}")
        print(f"Dados do Preco Diversos consultados com sucesso: {ticker}")
        return dados
    except Exception as e:
        logger.error(f"Erro na funcao pegar_df_preco_diversos: {e}")
        print(f"Erro na funcao pegar_df_preco_diversos: {e}")


def calcular_rentabilidade(df_preco:pd.DataFrame, data_ini:date, data_fim:date, carteira:list) -> str:
    """
    Calcula a rentabilidade de uma carteira de ações

    params:
    df_preco (pd.DataFrame): dataframe com os preços históricos das ações
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista das ações da carteira

    return:
    rendimento (str): rendimento calculado da carteira baseado no df_preco
    """
    rendimento = 0
    for ticker in carteira:
        try: 
            lst_preco = df_preco.loc[(df_preco.data.isin([data_ini,data_fim])) & (df_preco.ticker==ticker), 'fechamento'].values.tolist()
            rend = (lst_preco[1]/lst_preco[0] - 1)
            rendimento += rend * 1/len(carteira)
            logger.info(f'Rendimento {ticker}: {format(rend, ".2%")} - Preço Inicial: {format(lst_preco[0], "2.2f")}, Preço Final: {format(lst_preco[1], "2.2f")}')
            print(f'Rendimento {ticker}: {format(rend, ".2%")} - Preço Inicial: {format(lst_preco[0], "2.2f")}, Preço Final: {format(lst_preco[1], "2.2f")}')
        except Exception as e:
            logger.error(f"Erro na funcao calcular_rentabilidade: {e}")
            print(f"Erro na funcao calcular_rentabilidade: {e}")
            pass
    return rendimento

    