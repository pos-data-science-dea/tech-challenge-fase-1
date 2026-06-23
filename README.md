# Tech Challenge - Fase 1
Alunos: 
 - Artur Costa
 - Davi Tolentino



Repositorio do Tech Challenge da fase 1 da pos-graduacao em AI Scientist da FIAP.

O projeto analisa uma base de NPS de um e-commerce com o objetivo de entender quais fatores da jornada do cliente estao mais associados a satisfacao, detracao e possiveis pontos de ruptura da experiencia.

## Objetivo

Investigar, por meio de analise exploratoria de dados, quais variaveis operacionais, comerciais e de perfil ajudam a explicar o score de NPS dos clientes.

A analise busca responder perguntas como:

- Quais fatores parecem mais criticos para a satisfacao?
- O que mais diferencia clientes detratores de promotores?
- Existe algum ponto de ruptura na jornada do cliente?
- Que tipo de cliente tende a apresentar NPS mais alto ou mais baixo?
- Quais variaveis poderiam apoiar uma futura solucao preditiva sem gerar vazamento de informacao?

## Dados

Os dados estao organizados em:

- `dados/raw/desafio_nps_fase_1.csv`: base original do desafio.
- `dados/processed/desafio_nps_fase_1_feature_engineering.csv`: base com variaveis derivadas criadas durante a etapa de feature engineering.

Algumas variaveis derivadas usadas na EDA incluem:

- `flag_delay`: indica se houve atraso na entrega.
- `freight_rate`: proporcao do frete em relacao ao valor do item.
- `pct_desconto`: proporcao do desconto em relacao ao valor do item.
- `faixa_etaria`: faixa etaria do cliente.
- `classificacao`: classificacao do NPS em Detrator, Neutro e Promotor.

## Estrutura Do Repositorio

```text
.
├── dados/
│   ├── raw/
│   └── processed/
├── docs/
│   └── eda_mindmap.md
├── notebooks/
│   ├── 1. Sanity Check dos dados.ipynb
│   ├── 2. Feature engineering.ipynb
│   ├── 3. EDA.ipynb
│   └── eda/
│       └── eda_hypothesis.ipynb
├── src/
│   └── utils/
│       ├── sanity_utils.py
│       ├── eda_utils.py
│       └── data_viz.py
├── check.md
└── README.md
```

## Notebooks

A ordem recomendada de leitura e execucao e:

1. `notebooks/1. Sanity Check dos dados.ipynb`
   - Validacao inicial da base.
   - Verificacao de tipos, valores ausentes, duplicidades e distribuicoes.

2. `notebooks/2. Feature engineering.ipynb`
   - Criacao de variaveis derivadas para apoiar a analise.
   - Geracao da base processada em `dados/processed/`.

3. `notebooks/eda/eda_hypothesis.ipynb`
   - Analise exploratoria orientada por hipoteses.
   - Investigacao de fatores associados ao NPS.

O arquivo `docs/eda_mindmap.md` documenta o mapa de hipoteses usado para guiar a EDA.

## Hipoteses Da EDA

O notebook principal de EDA parte de blocos tematicos. O primeiro bloco investiga se aspectos logisticos impactam a satisfacao:

- H1: atraso na entrega reduz fortemente o NPS.
- H2: mais tentativas de entrega reduzem NPS.
- H3: tempo total de entrega importa menos que atraso percebido.
- H4: frete alto tem associacao com NPS.
- H5: frete alto associado a atraso causa mais insatisfacao que somente atraso.

As conclusoes devem ser interpretadas como evidencias exploratorias. Quando sao usados coeficientes de correlacao ou modelos simples de regressao, eles indicam associacao estatistica, nao causalidade definitiva.

## Utilitarios

O projeto possui funcoes auxiliares em `src/utils/` para evitar repeticao de codigo nos notebooks.

### `sanity_utils.py`

Funcoes para verificacoes iniciais da base, como:

- avaliacao de valores nulos;
- contagem de valores distintos;
- verificacao de duplicadas;
- tabelas de frequencia;
- graficos simples de histograma, boxplot e barras.

### `eda_utils.py`

Funcoes analiticas genericas para EDA:

- `summarize_numeric`
- `summarize_categorical`
- `compare_groups`
- `correlation_summary`
- `group_difference_summary`
- `simple_linear_regression_summary`

### `data_viz.py`

Funcoes de visualizacao padronizadas:

- `plot_comparative_histogram`
- `plot_boxplot`
- `plot_crosstab_heatmap`
- `plot_faceted_regression`
- `plot_nps_relationship`

## Como Reproduzir

1. Clone o repositorio.

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

3. Instale as dependencias usadas nos notebooks:

```bash
pip install pandas numpy matplotlib seaborn statsmodels jupyter
```

4. Abra o Jupyter:

```bash
jupyter notebook
```

5. Execute os notebooks na ordem recomendada.

## Observacoes Metodologicas

- O NPS e tratado como variavel principal de satisfacao.
- A classificacao de mercado usada quando necessario e:
  - Detrator: NPS menor ou igual a 6.
  - Neutro: NPS entre 7 e 8.
  - Promotor: NPS maior ou igual a 9.
- Analises de correlacao e regressao simples sao usadas para apoiar a interpretacao exploratoria.
- Resultados observacionais nao devem ser interpretados automaticamente como causalidade.
- Variaveis posteriores a pesquisa de NPS devem ser avaliadas com cuidado caso sejam usadas em modelos preditivos, pois podem gerar vazamento temporal.

## Status

O repositorio esta em desenvolvimento. As etapas de sanity check, feature engineering e EDA orientada por hipoteses estao estruturadas, com foco atual na interpretacao dos principais fatores associados ao NPS.
