{{ config(materialized='view') }}

/*
  Junta vendas com clientes e produtos, calcula métricas derivadas
  e prepara os dados para a camada de marts.
*/

with vendas as (
    select * from {{ ref('stg_vendas') }}
),

clientes as (
    select * from {{ ref('stg_clientes') }}
),

produtos as (
    select * from {{ ref('stg_produtos') }}
),

enriquecida as (
    select
        v.venda_id,
        v.data_venda,
        extract(year from v.data_venda) as ano,
        extract(month from v.data_venda) as mes,
        extract(quarter from v.data_venda) as trimestre,
        to_char(v.data_venda, 'YYYY-MM') as ano_mes,

        -- Cliente
        v.cliente_id,
        c.nome_cliente,
        c.cidade,
        c.provincia,
        c.tipo_cliente,

        -- Produto
        v.produto_id,
        p.nome_produto,
        p.categoria,
        p.fornecedor_principal,

        -- Métricas
        v.quantidade,
        v.preco_unitario,
        v.valor_bruto,
        v.desconto_percentual,
        v.valor_desconto,
        v.valor_liquido,
        round(v.valor_liquido / nullif(v.quantidade, 0), 2) as preco_medio_liquido,

        -- Dimensões de negócio
        v.canal,
        v.metodo_pagamento,
        v.vendedor,

        -- Flags úteis
        case when v.desconto_percentual > 0 then true else false end as teve_desconto,
        case
            when v.valor_liquido >= 100000 then 'Alto'
            when v.valor_liquido >= 20000 then 'Médio'
            else 'Baixo'
        end as faixa_valor

    from vendas v
    left join clientes c on v.cliente_id = c.cliente_id
    left join produtos p on v.produto_id = p.produto_id
)

select * from enriquecida
