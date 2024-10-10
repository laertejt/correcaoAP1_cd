import pandas as pd
import os
from pathlib import Path
from datetime import date, datetime
DATA_DIR = str(Path(os.path.dirname(__file__)).parent) + '/data'
LOG_DIR = str(Path(os.path.dirname(__file__)).parent) + '/logs'
import logging # Configuração básica do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=f'{LOG_DIR}/app.log',  # Nome do arquivo de log
                    filemode='a')  # 'w' sobrescreve o arquivo a cada execução, 'a' anexa ao arquivo
logger = logging.getLogger(__name__)
from pacote_bolsa.modulo_bolsa import (filtrar_duplicado,
                                      consultar_planilhao,
                                      pegar_df_preco_corrigido,  
                                      pegar_df_preco_diversos,
                                      calcular_rentabilidade)
# Parametros de entrada 
data_base = date(2023,4,3)
data_ini = date(2023,4,4)
data_fim = date(2024,4,1)
ticker='ibov'# Benchmark - Pegar preço do ibov
num_carteira = 10
lst_indicadores = ['roic', 'earning_yield']

def main():
  try:
    logger.info(f'Inicio do processo de formação da carteira.')
    print(f'Inicio do processo de formação da carteira.')
    dados = consultar_planilhao(data_base)
    planilhao = pd.DataFrame.from_dict(dados)
    planilhao.to_csv(DATA_DIR + '/planilhao.csv')
    planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
    df = filtrar_duplicado(planilhao)
    col = ['ticker', 'empresa', 'setor', 'volume', 'enterprise_value'] + lst_indicadores
    df = df.loc[:,col]
    # Seleção dos ativos baseados nos indicadores e qtde de ativos na carteira
    df['rank_rentabilidade'] = df[lst_indicadores[0]].rank()
    df['rank_desconto'] = df[lst_indicadores[1]].rank()
    df['rank'] = df.rank_rentabilidade + df.rank_desconto
    df = df.sort_values(['rank'], ascending=False)
    carteira = df.ticker.values[:num_carteira]
    logger.info(f'carteira formada: {carteira}')
    print(f'carteira formada: {carteira}')
    # Backtest de 12 meses
    df_preco = pegar_df_preco_corrigido(data_ini, data_fim, carteira)# Criação do df de precos para verificar a rentabilidade carteira
    df_preco['data'] = pd.to_datetime(df_preco['data']).dt.date # transformar para o formato de date
    logger.info("df_preco finalizado com sucesso")
    print("df_preco finalizado com sucesso")
    df_preco.to_csv(DATA_DIR + '/preco.csv')
    # Pegar Benchmark
    dados = pegar_df_preco_diversos(ticker, data_ini, data_fim)
    ibov = pd.DataFrame.from_dict(dados)
    ibov['data'] = pd.to_datetime(ibov['data']).dt.date # transformar para o formato de date
    ibov.to_csv(DATA_DIR + '/ibov.csv')
    lst_preco = ibov.loc[(ibov.data.isin([data_ini, data_fim])), 'fechamento'].values
    rend = (lst_preco[1]/lst_preco[0] - 1)
    rendimento = calcular_rentabilidade(df_preco, data_ini, data_fim, carteira)
    logger.info(f'Rendimento Final: {format(rendimento, "2.2%")}')
    print(f'Rendimento Final: {format(rendimento, "2.2%")}')
    logger.info(f'Rendimento {ticker}: {format(rend, ".2%")} - Preço Inicial: {format(lst_preco[0], "6.0f")}, Preço Final: {format(lst_preco[1], "6.0f")}')
    print(f'Rendimento {ticker}: {format(rend, ".2%")} - Preço Inicial: {format(lst_preco[0], "6.0f")}, Preço Final: {format(lst_preco[1], "6.0f")}')
  except Exception as e:
    logger.error(f"Erro na funcao principal: {e}")
    print(f"Erro na funcao principal: {e}")

if __name__ == "__main__":
  main()