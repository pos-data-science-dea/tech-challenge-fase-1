# Estratégia de Modelagem Preditiva — NPS

## 1. Abordagem escolhida: Regressão ou Classificação?

O desafio propõe duas abordagens possíveis para antecipar a satisfação do cliente:

- **Regressão:** estimar a nota de NPS em escala contínua (0–10)
- **Classificação:** categorizar diretamente o cliente como Detrator, Neutro ou Promotor

**O grupo optou por regressão.** As justificativas são técnicas e de negócio:

**Justificativas técnicas:**
- A EDA evidenciou relações aproximadamente lineares entre o `nps_score` e as principais variáveis operacionais — notavelmente `delivery_delay_days` (r = −0,60) e `complaints_count` (r = −0,50). Esse comportamento favorece modelos que exploram relações lineares como ponto de partida.
- Um modelo de regressão preserva a informação contínua do NPS. A classificação colapsa essa informação: um cliente com nota prevista de 1 e outro com nota prevista de 6 seriam ambos rotulados como "Detrator", embora representem graus muito diferentes de insatisfação.
- A classificação por categoria NPS sai de graça a partir da previsão contínua, aplicando a regra de negócio padrão à nota prevista (≤ 6 → Detrator, 7–8 → Neutro, ≥ 9 → Promotor). Um único modelo cobre as duas necessidades.

**Justificativas de negócio:**
- Saber que um cliente tende a dar nota 2 versus nota 5 é informação acionável para priorização de atendimento preventivo — a classificação binária ou trinária perde essa granularidade.
- Coeficientes de um modelo de regressão linear são diretamente interpretáveis: "cada dia adicional de atraso está associado a uma queda média de X pontos no NPS" é uma recomendação concreta para as áreas de logística e operações.
- Evita a necessidade de definir limiares de probabilidade de classe no treinamento, reduzindo decisões arbitrárias durante a modelagem.

---

## 2. Variável Alvo (Target)

**`nps_score`** — nota de satisfação atribuída pelo próprio cliente ao final da jornada de compra, em uma escala de 0 a 10.

- Coletada após o encerramento da experiência (pós-entrega e pós-atendimento)
- Representa a percepção declarada do cliente, sem intermediação da empresa
- A partir da nota prevista, a classificação é derivada com a mesma regra de mercado usada na EDA:
  - **Detrator:** NPS ≤ 6
  - **Neutro:** 7 ≤ NPS ≤ 8
  - **Promotor:** NPS ≥ 9

---

## 3. Variáveis de Entrada (Features)

As variáveis abaixo estão disponíveis antes da coleta do NPS e, portanto, não introduzem vazamento temporal.

### Variáveis com associação identificada na EDA

| Variável | Grupo | Correlação com NPS | Observação |
|---|---|---|---|
| `delivery_delay_days` | Logística | −0,60 | Principal driver de insatisfação; relação linear clara |
| `flag_delay` | Logística | — | Binário derivado; captura o efeito de qualquer atraso |
| `complaints_count` | Atendimento | −0,50 | Segundo maior sinal; relação linear com NPS |
| `customer_service_contacts` | Atendimento | −0,35 | Atenção: correlação de 0,75 com `complaints_count` (multicolinearidade) |
| `resolution_time_days` | Atendimento | −0,19 | Sinal fraco, mas relevante no contexto de atraso + atendimento lento |

> **Nota sobre multicolinearidade:** `complaints_count` e `customer_service_contacts` são altamente correlacionadas entre si (r = 0,75). Em modelos lineares, recomenda-se usar regularização (Ridge/Lasso) ou manter apenas a variável com maior poder preditivo individual (`complaints_count`).

### Variáveis sem associação direta identificada — incluir e testar

Mesmo sem associação bivariada clara com o NPS, estas variáveis podem contribuir no contexto multivariado ou em modelos não-lineares:

| Variável | Grupo |
|---|---|
| `delivery_time_days` | Logística |
| `freight_value` / `freight_rate` | Logística |
| `delivery_attempts` | Logística |
| `order_value` | Pedido |
| `items_quantity` | Pedido |
| `discount_value` / `pct_desconto` | Pedido |
| `payment_installments` | Pedido |
| `customer_age` | Perfil |
| `customer_region` | Perfil |
| `customer_tenure_months` | Perfil |

---

## 4. Variáveis Excluídas — Data Leakage

| Variável | Motivo da exclusão |
|---|---|
| `repeat_purchase_30d` | Evento posterior à pesquisa de NPS. A EDA mostrou que 92,2% dos promotores efetuaram recompra em 30 dias e 0% dos detratores. Usar essa variável como feature vazaria diretamente o resultado que o modelo tenta prever. |
| `csat_internal_score` | Apresenta correlação de 0,56 com NPS, mas o momento de cálculo desse indicador é desconhecido. Caso ele seja calculado com base no próprio NPS ou após a pesquisa, representa leakage. Sem clareza sobre a metodologia interna, a inclusão não é segura. |
| `classificacao` | Variável derivada diretamente do `nps_score` (Detrator/Neutro/Promotor). Incluí-la seria trivialmente leakage — é a target com outro nome. |

---

## 5. Algoritmos Candidatos

A estratégia é partir de um baseline interpretável e evoluir para modelos mais complexos apenas se o ganho de performance justificar a perda de interpretabilidade.

| Algoritmo | Papel | Vantagem principal |
|---|---|---|
| Regressão Linear (OLS) | Baseline | Totalmente interpretável; coeficientes são acionáveis pelo negócio |
| Ridge / Lasso | Baseline regularizado | Lida com multicolinearidade entre `complaints_count` e `customer_service_contacts`; Lasso elimina features irrelevantes automaticamente |
| Random Forest Regressor | Modelo não-linear | Captura interações entre variáveis; robusto a outliers; fornece feature importance |
| Gradient Boosting (XGBoost / LightGBM) | Modelo não-linear | Alta performance preditiva; feature importance interpretável via SHAP |

---

## 6. Separação dos Dados

- **Holdout:** 80% treino / 20% teste com `random_state` fixo para reprodutibilidade
- **Cross-validation:** K-Fold (k=5) sobre o conjunto de treino para seleção e comparação de modelos
- **Estratificação:** split estratificado por `classificacao` (Detrator/Neutro/Promotor) para garantir distribuição proporcional em treino e teste — importante dado o desbalanceamento entre classes

---

## 7. Métricas de Avaliação

### Regressão

| Métrica | O que mede | Por que usar |
|---|---|---|
| RMSE | Raiz do erro quadrático médio | Penaliza erros grandes; útil quando prever um detrator como promotor é muito custoso |
| MAE | Erro absoluto médio | Mais intuitivo para o negócio ("em média o modelo erra X pontos de NPS") |
| R² | Proporção da variância explicada | Referência geral de qualidade do ajuste |

### Classificação derivada

| Métrica | O que mede |
|---|---|
| Accuracy | Proporção de classificações corretas |
| F1-score por classe | Equilíbrio entre precisão e recall para cada segmento (Detrator / Neutro / Promotor) |
| Confusion Matrix | Onde o modelo erra (ex.: neutros classificados como detratores) |

> **Prioridade de negócio:** a métrica mais importante é o **recall na classe Detrator** — o custo de não identificar um detrator (falso negativo) é maior do que o custo de acionar preventivamente um cliente que seria neutro (falso positivo). Isso deve guiar o ajuste de threshold de classificação.
