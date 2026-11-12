{{ config(materialized='table') }}

select
    venda_id,
    data_venda,
    cliente_id,
    produto_id,
    quantidade,
    preco_unitario,
    valor_bruto,
    desconto_percentual,
    valor_desconto,
    valor_liquido,
    canal,
    metodo_pagamento,
    vendedor,
    teve_desconto,
    faixa_valor,
    current_timestamp as dbt_updated_at
from {{ ref('int_vendas_enriquecidas') }}
