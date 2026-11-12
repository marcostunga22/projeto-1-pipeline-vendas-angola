{{ config(materialized='table') }}

select
    categoria,
    count(*) as total_vendas,
    sum(quantidade) as quantidade_total,
    sum(valor_liquido) as valor_liquido_total,
    round(avg(valor_liquido), 2) as ticket_medio,
    round(100.0 * sum(valor_liquido) / sum(sum(valor_liquido)) over (), 2) as percentagem_do_total
from {{ ref('int_vendas_enriquecidas') }}
group by 1
order by valor_liquido_total desc
