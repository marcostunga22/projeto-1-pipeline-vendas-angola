{{ config(materialized='table') }}

select
    cliente_id,
    nome_cliente,
    cidade,
    provincia,
    tipo_cliente,
    data_registo,
    telefone,
    current_timestamp as dbt_updated_at
from {{ ref('stg_clientes') }}
