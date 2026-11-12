{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'clientes') }}
),

renamed as (
    select
        cliente_id,
        nome as nome_cliente,
        cidade,
        provincia,
        tipo_cliente,
        cast(data_registo as date) as data_registo,
        telefone,
        current_timestamp as loaded_at
    from source
)

select * from renamed
