{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'produtos') }}
),

renamed as (
    select
        produto_id,
        nome_produto,
        categoria,
        cast(preco_unitario as numeric(12,2)) as preco_unitario,
        unidade,
        fornecedor_principal,
        current_timestamp as loaded_at
    from source
)

select * from renamed
