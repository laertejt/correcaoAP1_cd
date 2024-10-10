import pandas as pd
import os
from pathlib import Path
from datetime import date, datetime
BASE_DIR = str(Path(os.path.dirname(__file__)).parent.parent)
LOG_DIR = str(Path(os.path.dirname(__file__)).parent.parent) + '/logs'
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
    planilhao.to_csv(BASE_DIR + '/data/planilhao.csv')
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
    df_preco.to_csv(BASE_DIR + '/data/preco.csv')
    # Pegar Benchmark
    dados = pegar_df_preco_diversos(ticker, data_ini, data_fim)
    ibov = pd.DataFrame.from_dict(dados)
    ibov['data'] = pd.to_datetime(ibov['data']).dt.date # transformar para o formato de date
    ibov.to_csv(BASE_DIR + '/data/ibov.csv')
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



# # Dados para o Graficos
# df_preco = pd.read_csv(BASE_DIR + '/data/preco.csv')
# df_preco["data"] = df_preco["data"].apply(lambda x:datetime.strptime(x, "%Y-%m-%d"))
# ibov = pd.read_csv(BASE_DIR + '/data/ibov.csv')
# ibov["data"] = ibov["data"].apply(lambda x:datetime.strptime(x, "%Y-%m-%d"))
# # dados das acoes
# kepl = df_preco.loc[df_preco.ticker=='KEPL3', ['data','fechamento']]
# petr = df_preco.loc[df_preco.ticker=='PETR4', ['data','fechamento']]


# # matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(kepl.data.values, kepl.fechamento.values, label='KEPL3')
# ax.set(xlabel='Ano', ylabel='Preço (R$)', title='Gráfico de Preço')
# ax.xaxis.set_major_locator(mdates.MonthLocator())  # Ticks principais em cada mês
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))  # Formato mês abreviado e ano
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y:.1f}'))
# # ax.legend(loc='upper left')
# # Criar um eixo Y secundário (ax2)
# ax2 = ax.twinx()
# ax2.plot(ibov.data.values, ibov.fechamento.values, label='IBOV', color="red")
# ax2.set_ylabel('Pontos')
# ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y / 1000:.0f} mil'))
# handles1, labels1 = ax.get_legend_handles_labels()  # Legenda do primeiro eixo (KEPL3)
# handles2, labels2 = ax2.get_legend_handles_labels()  # Legenda do segundo eixo (IBOV)
# ax.legend(handles=handles1 + handles2, labels=labels1 + labels2, loc='upper left')
# plt.xticks(rotation=45)  # Rotacionar rótulos das datas para melhor visualização
# plt.tight_layout()
# plt.show()

# #Grafico de Pizza
# planilhao = pd.read_csv(BASE_DIR + '/data/planilhao.csv')
# planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
# df = filtrar_duplicado(planilhao)
# df = df.loc[(df.volume>1000), :]
# lst_indicadores = ['roic', 'earning_yield']
# col = ['ticker', 'empresa', 'setor', 'volume', 'enterprise_value'] + lst_indicadores
# df = df.loc[:,col]
# # Seleção dos ativos baseados nos indicadores e qtde de ativos na carteira
# n = 10
# df['rank_rentabilidade'] = df['roic'].rank()
# df['rank_desconto'] = df['earning_yield'].rank()
# df['rank'] = df.rank_rentabilidade + df.rank_desconto
# df = df.sort_values(['rank'], ascending=False)
# df = df.iloc[:n]
# df_setor = df.groupby(['setor'])['setor'].value_counts().reset_index()
# # Criar o gráfico de pizza com base nas contagens por setor
# labels = df_setor['setor']  # Nomes dos setores
# sizes = df_setor['count']  # Tamanho (quantidade) de cada setor
# plt.figure(figsize=(8, 6))
# wedges, texts, autotexts = plt.pie(sizes, labels=None, autopct='%1.1f%%', startangle=90)
# plt.legend(wedges, labels, title="Setores", loc="upper right", bbox_to_anchor=(1.2, 1))
# plt.axis('equal')
# plt.title('Distribuição por Setores')
# plt.show()


# #Grafico de Barras
# df_ev = df[['empresa','enterprise_value']].reset_index(drop=True)
# df_ev = df_ev[~(df_ev.empresa=="PETR")].sort_values(['enterprise_value'], ascending=False)
# #plot
# fig, ax = plt.subplots()
# colors = ['skyblue', 'orange', 'lightgreen', 'lightcoral', 'violet', 'lightgray'] 
# ax.bar(df_ev.empresa.values, df_ev.enterprise_value.values, color=colors)
# ax.set_ylabel('Enterprise Value (R$)', fontsize=12)
# ax.set_title('Gráfico dos Valor de Mercado das Empresas', fontsize=14, fontweight='bold')
# plt.xticks(rotation=45, ha='right', fontsize=10)  
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e6:,.0f} MM'))
# ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7)
# for i, v in enumerate(df_ev.enterprise_value.values):
#     ax.text(i, v + (v * 0.01), f'{v/1e3:,.0f}', ha='center', va='bottom', fontsize=9)
# plt.tight_layout()
# plt.show()