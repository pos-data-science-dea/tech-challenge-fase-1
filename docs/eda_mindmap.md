# Mindmap da Análise Exploratória de Dados

São formuladas perguntas principais para serem respondidas durante a EDA:

- Quais fatores parecem mais críticos para a satisfação? 
- O que mais gera detratores? (ou O que separa detratores de promotores?)
- Existe algum “ponto de ruptura” na experiência do cliente? Qual evento operacional explica esse ponto?
- Que tipo de cliente tende a ter NPS mais alto ou mais baixo?

Uma outra pergunta importante de ser respondida nessa etapa é: Quais variáveis podem ser usadas para explicar o fenômeno do NPS antes da pesquisa. Por exemplo, a variável que mostra se o cliente efetuou uma recompra num intervalo de 30 dias é interessante para estudar o histórico comportamental dos promotores, por exemplo, mas não pode ser usada como variável num podelo de predição de NPS, pois geraria vazamento. 

Para responder essas perguntas de forma orientada às variáveis disponíveis, é formulado um mindmap de hipóteses, que, quando analisadas, podem indicar as melhores respostas possíveis dado o comportamento observado na base.

Para análises de detrator x ofensor, considera-se quando necessário, a definição de mercado: 

- Detrator: NPS <=6
- Neutro: 7<= NPS<9
- Promotor: NPS >= 9

# Mindmap de Hipoteses -

## 1. Logistica impacta satisfação?

- **H1:** Atraso na entrega reduz fortemente o NPS.
- **H2:** Mais tentativas de entrega reduzem NPS.
- **H3:** Tempo total de entrega importa menos que atraso percebido?
- **H4:** Frete alto + atraso impacta mais no NPS do que somente atraso.
- **H5:** Frete alto + atraso impacta mais no NPS do que somente atraso.

## 2. Impacto do atendimento na satisfação

- **H6:** Mais contatos com atendimento indicam maior chance de detrator/menor NPS
- **H7:** Maior tempo de resolutividade reduz NPS.
- **H8:** Reclamacoes sao mais impactantes em NPS que contatos simples.
- **H9:** Atendimento rapido pode recuperar parcialmente clientes com problema logistico.

## 3. Perfil do pedido impacta a satisfação?

- **H10:** Pedidos de maior valor geram maior expectativa e menor tolerancia a falhas - Ou seja, pedidos de maiores valores tem menor NPS quando atrasados, por exemplo, em comparação com a média
- **H11:** Maior quantidade de itens aumenta risco operacional (Atrasos, por exemplo)
- **H12:** Descontos reduzem insatisfaçãoo ou mascaram possíveis problemas.
- **H13:** Muitas parcelas podem estar associadas a perfis com comportamento diferente.

## 4. Perfil do cliente influencia NPS?

- **H14:** Clientes antigos sao mais tolerantes a falhas como atrasos ou várias tentativas de entrega.
- **H15:** Clientes novos tem NPS mais sensivel a primeira experiencia.
- **H16:** Idade e regiao podem revelar segmentos com expectativas diferentes
    H16.1: Clientes mais jovens reagem de forma diferente a atrasos
    H16.2: Clientes de regiões espcíficas são mais tolerantes a atraso?
- **H17:** Diferencas regionais podem refletir operacao logistica local.

## 5. Indicadores internos se relacionam com NPS?
Análises que ajudam a analisar o histórico, mas não necessariamente podem ser usadas como features em modelo preditivo.

- **H18:** Recompra em 30 dias valida satisfacao real.
- **H19:** Ausencia de recompra pode ser consequencia de experiencia ruim.


## 6. Pontos de ruptura na jornada

- **H20:** Existe um limite de atraso a partir do qual o NPS cai de forma mais significativa.
- **H21:** A partir de certo numero de reclamacoes, os clientes tendem a ser mais detratores.
- **H22:** Resoluçaõ demorada combinada com atraso cria efeito pior que cada fator isolado.
- **H24:** Clientes com frete alto e atraso tem percepção pior
## 

A partir da análise dessas hipóteses, entende-se que é possível responder com qualidade às perguntas que balizam a Análise Exploratória voltada para NPS. 
