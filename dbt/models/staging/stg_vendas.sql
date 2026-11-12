{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'vendas') }}
),

renamed as (
    select
        venda_id,
        cliente_id,
        produto_id,
        cast(data_venda as date) as data_venda,
        cast(quantidade as integer) as quantidade,
        cast(preco_unitario as numeric(12,2)) as preco_unitario,
        cast(valor_bruto as numeric(14,2)) as valor_bruto,
        cast(desconto_percentual as numeric(5,4)) as desconto_percentual,
        cast(valor_desconto as numeric(12,2)) as valor_desconto,
        cast(valor_liquido as numeric(14,2)) as valor_liquido,
        canal,
        metodo_pagamento,
        vendedor,
        current_timestamp as loaded_at
    from source
)

select * from renamed
