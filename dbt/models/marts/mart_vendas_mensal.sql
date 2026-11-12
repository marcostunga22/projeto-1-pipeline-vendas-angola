{{ config(materialized='table') }}

select
    ano,
    mes,
    ano_mes,
    count(*) as total_vendas,
    count(distinct cliente_id) as clientes_ativos,
    sum(quantidade) as quantidade_total,
    sum(valor_bruto) as valor_bruto_total,
    sum(valor_desconto) as desconto_total,
    sum(valor_liquido) as valor_liquido_total,
    round(avg(valor_liquido), 2) as ticket_medio
from {{ ref('int_vendas_enriquecidas') }}
group by 1, 2, 3
order by ano, mes
