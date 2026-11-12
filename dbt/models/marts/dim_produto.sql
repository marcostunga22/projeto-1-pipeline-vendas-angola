{{ config(materialized='table') }}

select
    produto_id,
    nome_produto,
    categoria,
    preco_unitario,
    unidade,
    fornecedor_principal,
    current_timestamp as dbt_updated_at
from {{ ref('stg_produtos') }}
