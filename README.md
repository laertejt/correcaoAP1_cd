# AnÃ¡lise de Carteiras de AÃ§Ãµes com Base em ROE e Magic Formula

Este projeto tem como objetivo criar uma carteira de aÃ§Ãµes com base nos 10 papÃ©is com maior **ROE (Return on Equity)** e comparÃ¡-la com o desempenho do **IBOVESPA** e da estratÃ©gia **Magic Formula** de Joel Greenblatt no perÃ­odo de **01 de abril de 2023** atÃ© **01 de abril de 2024**.

## SumÃ¡rio

- [DescriÃ§Ã£o do Projeto](#descriÃ§Ã£o-do-projeto)
- [Requisitos](#requisitos)
- [InstalaÃ§Ã£o](#instalaÃ§Ã£o)
- [ConfiguraÃ§Ã£o](#configuraÃ§Ã£o)
- [Uso](#uso)
- [Metodologia](#metodologia)
- [Resultados Esperados](#resultados-esperados)
- [ContribuiÃ§Ã£o](#contribuiÃ§Ã£o)
- [LicenÃ§a](#licenÃ§a)

## DescriÃ§Ã£o do Projeto

O script em Python realiza as seguintes tarefas:

1. **Coleta de Dados**: ObtÃ©m dados financeiros das aÃ§Ãµes a partir da API do LaboratÃ³rio de FinanÃ§as, filtrando por ROE e outros indicadores conforme necessÃ¡rio.
2. **Montagem da Carteira**:
   - **Carteira ROE**: Seleciona as 10 aÃ§Ãµes com os maiores valores de ROE.
   - **Carteira Magic Formula**: Aplica a fÃ³rmula de Joel Greenblatt, analisando conjuntamente o ROIC e o Earning Yield.
3. **AnÃ¡lise de Desempenho**:
   - Calcula o rendimento das carteiras no perÃ­odo especificado.
   - Compara o desempenho das carteiras com o IBOVESPA.
   - Identifica quais aÃ§Ãµes superaram ou nÃ£o o rendimento do Ã­ndice.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `pandas`
  - `requests`
  - `python-dotenv`

## InstalaÃ§Ã£o

1. **Clone o repositÃ³rio ou copie os arquivos para um diretÃ³rio local**.

2. **Crie um ambiente virtual** (opcional, mas recomendado):

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependÃªncias**:

   ```bash
   pip install -r requirements.txt
   ```

   **Caso nÃ£o tenha um arquivo `requirements.txt`, instale as bibliotecas diretamente**:

   ```bash
   pip install pandas requests python-dotenv
   ```

## ConfiguraÃ§Ã£o

1. **Obtenha o Token JWT**:

   VocÃª precisarÃ¡ de um token JWT vÃ¡lido para acessar a API do LaboratÃ³rio de FinanÃ§as. Certifique-se de ter o token de acesso.

2. **Crie um arquivo `.env`** na raiz do projeto e adicione o seu token:

   ```
   TOKEN=seu_token_jwt_aqui
   ```

   Substitua `seu_token_jwt_aqui` pelo seu token real.

3. **Adicione o arquivo `.env` ao seu `.gitignore`** (se aplicÃ¡vel):

   Se vocÃª estiver usando o Git, Ã© recomendÃ¡vel adicionar o arquivo `.env` ao `.gitignore` para evitar que o token seja enviado para um repositÃ³rio remoto.

   ```
   # .gitignore
   .env
   ```

## Uso

1. **Execute o script**:

   ```bash
   python main.py
   ```

2. **Aguarde a execuÃ§Ã£o**:

   O script irÃ¡:

   - Obter os dados financeiros das aÃ§Ãµes na data base especificada.
   - Calcular o rendimento do IBOVESPA no perÃ­odo.
   - Selecionar as top 10 aÃ§Ãµes por ROE e pela Magic Formula.
   - Calcular os rendimentos das aÃ§Ãµes selecionadas.
   - Comparar os rendimentos das carteiras com o IBOVESPA.
   - Exibir os resultados no console.

## Metodologia

### 1. Coleta de Dados

- **PlanilhÃ£o**: ObtÃ©m dados financeiros das empresas, como ROE, ROIC, Earning Yield, etc., na data base de 03/04/2023.
- **PreÃ§os HistÃ³ricos**: ObtÃ©m os preÃ§os ajustados das aÃ§Ãµes selecionadas e do IBOVESPA para o perÃ­odo de 03/04/2023 a 01/04/2024.

### 2. SeleÃ§Ã£o de AÃ§Ãµes

- **Carteira ROE**:
  - Seleciona as 10 aÃ§Ãµes com os maiores valores de ROE.
  - Remove duplicatas, mantendo a aÃ§Ã£o com maior volume.
- **Carteira Magic Formula**:
  - Exclui setores nÃ£o aplicÃ¡veis (bancos, seguros e financeiros).
  - Calcula o ranking combinado de ROIC e Earning Yield.
  - Seleciona as 10 aÃ§Ãµes com melhor posiÃ§Ã£o no ranking.

### 3. AnÃ¡lise de Desempenho

- **CÃ¡lculo de Rendimentos**:
  - Calcula o rendimento percentual de cada aÃ§Ã£o no perÃ­odo.
  - Calcula o rendimento mÃ©dio das carteiras.
- **ComparaÃ§Ã£o com o IBOVESPA**:
  - Compara o rendimento individual e mÃ©dio das carteiras com o rendimento do IBOVESPA.
  - Identifica quais aÃ§Ãµes superaram o Ã­ndice.

## Resultados Esperados

O script irÃ¡ fornecer:

- **Rendimento do IBOVESPA** no perÃ­odo analisado.
- **Rendimentos individuais** das aÃ§Ãµes nas carteiras ROE e Magic Formula.
- **Lista de aÃ§Ãµes** que superaram ou nÃ£o o IBOVESPA em cada carteira.
- **Rendimento mÃ©dio** das carteiras.
- **ConclusÃ£o** sobre o desempenho das carteiras em relaÃ§Ã£o ao IBOVESPA.

## ContribuiÃ§Ã£o

ContribuiÃ§Ãµes sÃ£o bem-vindas! Sinta-se Ã  vontade para abrir issues ou enviar pull requests.

## LicenÃ§a

Este projeto Ã© de uso livre para fins educacionais e nÃ£o possui uma licenÃ§a especÃ­fica.

---

**AtenÃ§Ã£o**: Este script Ã© fornecido para fins educacionais e nÃ£o constitui recomendaÃ§Ã£o de investimento. Sempre consulte um profissional qualificado antes de tomar decisÃµes financeiras.# correcaoAP1_cd
