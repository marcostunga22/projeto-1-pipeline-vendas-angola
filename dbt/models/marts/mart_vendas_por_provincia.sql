{{ config(materialized='table') }}

select
    provincia,
    count(distinct cliente_id) as total_clientes,
    count(*) as total_vendas,
    sum(quantidade) as quantidade_total,
    sum(valor_bruto) as valor_bruto_total,
    sum(valor_desconto) as desconto_total,
    sum(valor_liquido) as valor_liquido_total,
    round(avg(valor_liquido), 2) as ticket_medio,
    round(sum(valor_liquido) / nullif(count(*), 0), 2) as valor_medio_por_venda
from {{ ref('int_vendas_enriquecidas') }}
group by 1
order by valor_liquido_total desc
