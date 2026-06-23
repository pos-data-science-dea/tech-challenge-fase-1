# Tech Challenge - Fase 1

Alunos:

* Artur Costa
* Davi Tolentino

Repositório do Tech Challenge da Fase 1 da pós-graduação em AI Scientist da FIAP.

O projeto analisa uma base de NPS de um e-commerce com o objetivo de entender quais fatores da jornada do cliente estão mais associados à satisfação, à detratação e a possíveis pontos de ruptura da experiência.

## Objetivo

Investigar, por meio de análise exploratória de dados, quais variáveis operacionais, comerciais e de perfil ajudam a explicar o score de NPS dos clientes.

A análise busca responder perguntas como:

* Quais fatores parecem mais críticos para a satisfação?
* O que mais diferencia clientes detratores de promotores?
* Existe algum ponto de ruptura na jornada do cliente?
* Que tipo de cliente tende a apresentar NPS mais alto ou mais baixo?
* Quais variáveis poderiam apoiar uma futura solução preditiva sem gerar vazamento de informação?

## Dados

Os dados estão organizados em:

* `dados/raw/desafio_nps_fase_1.csv`: base original do desafio.
* `dados/processed/desafio_nps_fase_1_feature_engineering.csv`: base com variáveis derivadas criadas durante a etapa de feature engineering.

Algumas variáveis derivadas usadas na EDA incluem:

* `flag_delay`: indica se houve atraso na entrega.
* `freight_rate`: proporção do frete em relação ao valor do item.
* `pct_desconto`: proporção do desconto em relação ao valor do item.
* `faixa_etaria`: faixa etária do cliente.
* `classificacao`: classificação do NPS em Detrator, Neutro e Promotor.

## Estrutura do Repositório

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
└── README.md
```

## Notebooks

A ordem recomendada de leitura e execução é:

1. `notebooks/1. Sanity Check dos dados.ipynb`

   * Validação inicial da base.
   * Verificação de tipos, valores ausentes, duplicidades e distribuições.

2. `notebooks/2. Feature engineering.ipynb`

   * Criação de variáveis derivadas para apoiar a análise.
   * Geração da base processada em `dados/processed/`.

3. `notebooks/eda/eda_hypothesis.ipynb`

   * Análise exploratória orientada por hipóteses.
   * Investigação de fatores associados ao NPS.

O arquivo `docs/eda_mindmap.md` documenta o mapa de hipóteses usado para guiar a EDA.

## Hipóteses da EDA

O notebook principal de EDA parte de blocos temáticos. O primeiro bloco investiga se aspectos logísticos impactam a satisfação:

* H1: atraso na entrega reduz fortemente o NPS.
* H2: mais tentativas de entrega reduzem o NPS.
* H3: tempo total de entrega importa menos que o atraso percebido.
* H4: frete alto tem associação com o NPS.
* H5: frete alto associado a atraso causa mais insatisfação que somente atraso.

As conclusões devem ser interpretadas como evidências exploratórias. Quando são usados coeficientes de correlação ou modelos simples de regressão, eles indicam associação estatística, não causalidade definitiva.

## Utilitários

O projeto possui funções auxiliares em `src/utils/` para evitar repetição de código nos notebooks.

### `sanity_utils.py`

Funções para verificações iniciais da base, como:

* avaliação de valores nulos;
* contagem de valores distintos;
* verificação de duplicadas;
* tabelas de frequência;
* gráficos simples de histograma, boxplot e barras.

### `eda_utils.py`

Funções analíticas genéricas para EDA:

* `summarize_numeric`
* `summarize_categorical`
* `compare_groups`
* `correlation_summary`
* `group_difference_summary`
* `simple_linear_regression_summary`

### `data_viz.py`

Funções de visualização padronizadas:

* `plot_comparative_histogram`
* `plot_boxplot`
* `plot_crosstab_heatmap`
* `plot_faceted_regression`
* `plot_nps_relationship`

## Como Reproduzir

1. Clone o repositório.

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

3. Instale as dependências usadas nos notebooks:

```bash
pip install pandas numpy matplotlib seaborn statsmodels jupyter
```

4. Abra o Jupyter:

```bash
jupyter notebook
```

5. Execute os notebooks na ordem recomendada.

## Observações Metodológicas

* O NPS é tratado como variável principal de satisfação.
* A classificação de mercado usada quando necessário é:

  * Detrator: NPS menor ou igual a 6.
  * Neutro: NPS entre 7 e 8.
  * Promotor: NPS maior ou igual a 9.
* Análises de correlação e regressão simples são usadas para apoiar a interpretação exploratória.
* Resultados observacionais não devem ser interpretados automaticamente como causalidade.
* Variáveis posteriores à pesquisa de NPS devem ser avaliadas com cuidado caso sejam usadas em modelos preditivos, pois podem gerar vazamento temporal.

## Status

O repositório está em desenvolvimento. As etapas de sanity check, feature engineering e EDA orientada por hipóteses estão estruturadas, com foco atual na interpretação dos principais fatores associados ao NPS.

