{{ config(materialized='table') }}

/*
  Dimensão de data simples gerada a partir das vendas.
  Em projetos maiores normalmente usa-se uma tabela de calendário completa.
*/

with datas as (
    select distinct
        data_venda as data,
        extract(year from data_venda)::int as ano,
        extract(month from data_venda)::int as mes,
        extract(day from data_venda)::int as dia,
        extract(quarter from data_venda)::int as trimestre,
        extract(dow from data_venda)::int as dia_semana_num,
        to_char(data_venda, 'Day') as dia_semana,
        to_char(data_venda, 'Month') as nome_mes,
        to_char(data_venda, 'YYYY-MM') as ano_mes
    from {{ ref('stg_vendas') }}
)

select
    data,
    ano,
    mes,
    dia,
    trimestre,
    dia_semana_num,
    trim(dia_semana) as dia_semana,
    trim(nome_mes) as nome_mes,
    ano_mes,
    case when dia_semana_num in (0, 6) then true else false end as is_fim_de_semana
from datas
order by data
