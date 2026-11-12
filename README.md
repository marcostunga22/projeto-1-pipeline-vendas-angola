# Projeto 1 — Pipeline Batch Local  
### Pipeline de Análise de Vendas — Contexto Angolano

**Stack:** PostgreSQL · Apache Airflow · dbt · Docker Compose · Python

---

## Objetivo

Construir um pipeline de dados batch completo e local que demonstra os fundamentos sólidos de Engenharia de Dados:

- Ingestão confiável de dados
- Orquestração com Airflow
- Transformação e modelagem dimensional com dbt
- Arquitetura em camadas (Staging → Intermediate → Marts)
- Ambiente 100% reprodutível com Docker

Este projeto usa **dados sintéticos realistas** de uma distribuidora angolana fictícia (**Distribuidora Kwanza Comercial**), com cidades, produtos e nomes angolanos.

---

## Arquitetura

```
CSV (clientes, produtos, vendas)
          │
          ▼
   ┌──────────────┐
   │   Airflow    │  ← Orquestração
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PostgreSQL  │
   │  schema raw  │  ← Bronze / Raw
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │     dbt      │
   │  staging     │  ← Views limpas e tipadas
   │  intermediate│  ← Lógica de negócio
   │  marts       │  ← Star Schema + agregações
   └──────────────┘
```

### Camadas dbt

| Camada        | Schema       | Materialização | Conteúdo                                      |
|---------------|--------------|----------------|-----------------------------------------------|
| Staging       | `staging`    | view           | `stg_clientes`, `stg_produtos`, `stg_vendas` |
| Intermediate  | `intermediate`| view          | `int_vendas_enriquecidas`                     |
| Marts         | `marts`      | table          | Dimensões + Fact + Marts analíticos           |

### Modelo Dimensional (Star Schema)

- **Fact**: `fct_vendas`
- **Dimensões**: `dim_cliente`, `dim_produto`, `dim_data`
- **Marts analíticos**:
  - `mart_vendas_por_provincia`
  - `mart_vendas_por_categoria`
  - `mart_vendas_mensal`

---

## Pré-requisitos

- Docker Desktop (ou Docker Engine + Docker Compose)
- Pelo menos 4 GB de RAM disponíveis para os containers
- Portas livres: `5432` (Postgres) e `8080` (Airflow)

---

## Como executar

### 1. Clone / entre na pasta do projeto

```bash
cd projeto-1-pipeline-vendas-angola
```

### 2. Defina o AIRFLOW_UID (Linux/Mac)

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

No Windows (PowerShell) podes criar o ficheiro `.env` manualmente com:

```
AIRFLOW_UID=50000
```

### 3. Suba a stack

```bash
docker compose up --build -d
```

Na primeira execução demora alguns minutos (build da imagem + inicialização do Airflow).

### 4. Acede ao Airflow

- URL: http://localhost:8080
- Utilizador: `admin`
- Password: `admin`

### 5. Ativa e corre a DAG

1. No Airflow UI, encontra a DAG `pipeline_vendas_angola`
2. Ativa o toggle (unpause)
3. Clica em **Trigger DAG**

A DAG faz:

1. Gera os dados sintéticos (se ainda não existirem)
2. Carrega os CSVs para o schema `raw`
3. Executa `dbt run`
4. Executa `dbt test`
5. Gera documentação dbt

---

## Estrutura do Projeto

```
projeto-1-pipeline-vendas-angola/
├── dags/
│   └── pipeline_vendas.py          # DAG principal
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       ├── intermediate/
│       └── marts/
├── data/
│   └── raw/                        # CSVs gerados
├── scripts/
│   ├── gerar_dados.py              # Gera dataset angolano
│   └── init-db.sh                  # Inicializa schemas no Postgres
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Dataset

Gerado sinteticamente com contexto angolano:

- **180 clientes** (nomes angolanos, cidades reais)
- **29 produtos** (combustíveis, construção, agrícolas, bens de consumo, equipamentos)
- **3.500 vendas** (2023–2025)
- Moeda: **Kwanza (AOA)**
- Cidades: Luanda, Benguela, Huambo, Lobito, Lubango, Malanje, Cabinda, etc.

Para regenerar os dados:

```bash
python scripts/gerar_dados.py
```

---

## Consultas úteis (após o pipeline correr)

Conecta-te ao PostgreSQL:

```bash
docker exec -it vendas_postgres psql -U dw_user -d vendas_dw
```

Exemplos:

```sql
-- Top províncias por faturação
SELECT * FROM marts.mart_vendas_por_provincia;

-- Vendas por categoria
SELECT * FROM marts.mart_vendas_por_categoria;

-- Evolução mensal
SELECT * FROM marts.mart_vendas_mensal ORDER BY ano, mes;

-- Fact + dimensões
SELECT 
    f.venda_id,
    d.data,
    c.nome_cliente,
    c.provincia,
    p.nome_produto,
    p.categoria,
    f.valor_liquido
FROM marts.fct_vendas f
JOIN marts.dim_cliente c ON f.cliente_id = c.cliente_id
JOIN marts.dim_produto p ON f.produto_id = p.produto_id
JOIN marts.dim_data d ON f.data_venda = d.data
LIMIT 20;
```

---

## Credenciais

| Serviço       | Host / URL              | Utilizador | Password  |
|---------------|-------------------------|------------|-----------|
| Airflow UI    | http://localhost:8080   | admin      | admin     |
| PostgreSQL DW | localhost:5432          | dw_user    | dw_pass   |
| PostgreSQL    | localhost:5432          | airflow    | airflow   |

Base de dados do warehouse: `vendas_dw`

---

## O que este projeto demonstra

- Domínio de fundamentos (ingestão, orquestração, transformação)
- Uso correto de dbt (camadas, testes, documentação)
- Modelagem dimensional (Star Schema)
- Ambiente reprodutível com Docker
- Código organizado e legível (pronto para portfólio)

---

## Próximos passos (Projeto 2 e 3)

- **Projeto 2**: Levar este pipeline para a AWS (S3 + Glue + Athena/Redshift + Airflow + CI/CD)
- **Projeto 3**: Pipeline de streaming com Kafka + Spark Structured Streaming

---

**Autor:** Projeto desenvolvido no âmbito do Módulo 16 — Fundação  
**Contexto:** Pipeline de Análise de Vendas com dados angolanos
