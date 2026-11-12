#!/usr/bin/env python3
"""
Gera dataset sintético de vendas com contexto angolano.
Empresa fictícia: Distribuidora Kwanza Comercial (DKC)
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configurações
NUM_CLIENTES = 180
NUM_PRODUTOS = 45
NUM_VENDAS = 3500
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Dados angolanos realistas
CIDADES = [
    "Luanda", "Benguela", "Huambo", "Lobito", "Lubango",
    "Malanje", "Cabinda", "Uíge", "Soyo", "N'dalatando",
    "Menongue", "Saurimo", "Sumbe", "Caxito", "Dundo"
]

PROVINCIAS = {
    "Luanda": "Luanda",
    "Benguela": "Benguela",
    "Huambo": "Huambo",
    "Lobito": "Benguela",
    "Lubango": "Huíla",
    "Malanje": "Malanje",
    "Cabinda": "Cabinda",
    "Uíge": "Uíge",
    "Soyo": "Zaire",
    "N'dalatando": "Cuanza Norte",
    "Menongue": "Cuando Cubango",
    "Saurimo": "Lunda Sul",
    "Sumbe": "Cuanza Sul",
    "Caxito": "Bengo",
    "Dundo": "Lunda Norte"
}

NOMES_MASCULINOS = [
    "João", "António", "Manuel", "José", "Carlos", "Pedro", "Francisco",
    "Miguel", "Paulo", "Domingos", "Sebastião", "Rui", "Fernando", "André",
    "Nelson", "Hélder", "Edson", "Wilson", "Bruno", "Sérgio", "Vítor",
    "Daniel", "Ricardo", "Eduardo", "Agostinho", "Mateus", "Isaías"
]

NOMES_FEMININOS = [
    "Maria", "Ana", "Isabel", "Teresa", "Lúcia", "Paula", "Helena",
    "Carla", "Sandra", "Cristina", "Sofia", "Beatriz", "Marta", "Joana",
    "Filomena", "Rosa", "Celeste", "Esperança", "Amélia", "Conceição",
    "Fátima", "Graça", "Irene", "Juliana", "Natália", "Vera"
]

SOBRENOMES = [
    "da Silva", "dos Santos", "Fernandes", "Costa", "Rodrigues", "Pereira",
    "Oliveira", "Martins", "Gonçalves", "Sousa", "Almeida", "Nascimento",
    "Lopes", "Carvalho", "Mendes", "Barbosa", "Ribeiro", "Pinto",
    "Correia", "Dias", "Teixeira", "Monteiro", "Cunha", "Moreira",
    "Cardoso", "Freitas", "Vieira", "Campos", "Ramos", "Afonso",
    "Quintão", "Bento", "Kassoma", "Ngola", "Kiala", "Manuel",
    "Domingos", "Francisco", "Pedro", "António"
]

CATEGORIAS_PRODUTOS = {
    "Combustíveis": [
        ("Gasóleo", 850.0, 1200.0),
        ("Gasolina Super", 920.0, 1350.0),
        ("Petróleo Iluminante", 680.0, 950.0),
        ("Óleo Lubrificante 20W50", 4500.0, 7800.0),
    ],
    "Materiais de Construção": [
        ("Cimento Portland 50kg", 4800.0, 6200.0),
        ("Ferro de Construção 12mm", 18500.0, 24000.0),
        ("Tijolo Cerâmico", 85.0, 140.0),
        ("Areia de Construção (m³)", 12000.0, 18000.0),
        ("Brita (m³)", 15000.0, 22000.0),
        ("Tinta Acrílica 18L", 28000.0, 38000.0),
    ],
    "Produtos Agrícolas": [
        ("Milho Amarelo (saco 50kg)", 8500.0, 12500.0),
        ("Feijão Catete (saco 25kg)", 14000.0, 19500.0),
        ("Arroz Agulha (saco 25kg)", 16000.0, 22000.0),
        ("Farinha de Mandioca (saco 50kg)", 9500.0, 14000.0),
        ("Café Robusta (kg)", 2800.0, 4200.0),
        ("Amendoim (saco 25kg)", 11000.0, 16500.0),
    ],
    "Bens de Consumo": [
        ("Óleo Alimentar 5L", 4200.0, 5800.0),
        ("Açúcar Refinado 1kg", 650.0, 950.0),
        ("Sabão em Pó 2kg", 1800.0, 2600.0),
        ("Água Mineral 20L", 1200.0, 1800.0),
        ("Refrigerante 2L", 850.0, 1300.0),
        ("Cerveja Nacional (cx 24)", 9500.0, 13500.0),
        ("Leite em Pó 400g", 2200.0, 3100.0),
        ("Massas Alimentícias 500g", 480.0, 720.0),
    ],
    "Equipamentos": [
        ("Gerador 5kVA", 450000.0, 680000.0),
        ("Bomba de Água 1HP", 85000.0, 125000.0),
        ("Motosserra Profissional", 95000.0, 145000.0),
        ("Soldadora Elétrica", 120000.0, 185000.0),
        ("Compressor de Ar", 78000.0, 115000.0),
    ]
}

CANAIS = ["Retalho", "Grossista", "Contrato Público", "Exportação Regional"]
METODOS_PAGAMENTO = ["Transferência", "Dinheiro", "Cheque", "Crédito 30 dias", "Crédito 60 dias"]


def gerar_nome():
    if random.random() < 0.55:
        return f"{random.choice(NOMES_MASCULINOS)} {random.choice(SOBRENOMES)}"
    return f"{random.choice(NOMES_FEMININOS)} {random.choice(SOBRENOMES)}"


def gerar_clientes():
    clientes = []
    for i in range(1, NUM_CLIENTES + 1):
        cidade = random.choice(CIDADES)
        clientes.append({
            "cliente_id": f"CLI-{i:04d}",
            "nome": gerar_nome(),
            "cidade": cidade,
            "provincia": PROVINCIAS[cidade],
            "tipo_cliente": random.choices(
                ["Pessoa Singular", "Empresa", "Instituição Pública"],
                weights=[0.45, 0.40, 0.15]
            )[0],
            "data_registo": (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 900))).strftime("%Y-%m-%d"),
            "telefone": f"+244 9{random.randint(1, 9)}{random.randint(1000000, 9999999)}"
        })
    return clientes


def gerar_produtos():
    produtos = []
    pid = 1
    for categoria, itens in CATEGORIAS_PRODUTOS.items():
        for nome, preco_min, preco_max in itens:
            produtos.append({
                "produto_id": f"PRD-{pid:03d}",
                "nome_produto": nome,
                "categoria": categoria,
                "preco_unitario": round(random.uniform(preco_min, preco_max), 2),
                "unidade": "un" if "kg" not in nome.lower() and "m³" not in nome and "L" not in nome else "saco/kg/L",
                "fornecedor_principal": random.choice([
                    "Sonangol", "CIF", "Cuca", "Refriango", "Local Agro",
                    "Importadora Atlântico", "Construtora Nacional", "Petromar"
                ])
            })
            pid += 1
    return produtos


def gerar_vendas(clientes, produtos):
    vendas = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 10, 31)
    delta = (end_date - start_date).days

    for i in range(1, NUM_VENDAS + 1):
        cliente = random.choice(clientes)
        produto = random.choice(produtos)
        data_venda = start_date + timedelta(days=random.randint(0, delta))
        quantidade = random.randint(1, 50) if produto["categoria"] != "Equipamentos" else random.randint(1, 5)
        desconto = random.choices([0, 0.05, 0.10, 0.15], weights=[0.6, 0.25, 0.10, 0.05])[0]
        valor_bruto = round(produto["preco_unitario"] * quantidade, 2)
        valor_desconto = round(valor_bruto * desconto, 2)
        valor_liquido = round(valor_bruto - valor_desconto, 2)

        vendas.append({
            "venda_id": f"VND-{i:05d}",
            "cliente_id": cliente["cliente_id"],
            "produto_id": produto["produto_id"],
            "data_venda": data_venda.strftime("%Y-%m-%d"),
            "quantidade": quantidade,
            "preco_unitario": produto["preco_unitario"],
            "valor_bruto": valor_bruto,
            "desconto_percentual": desconto,
            "valor_desconto": valor_desconto,
            "valor_liquido": valor_liquido,
            "canal": random.choice(CANAIS),
            "metodo_pagamento": random.choice(METODOS_PAGAMENTO),
            "vendedor": gerar_nome()
        })
    return vendas


def salvar_csv(dados, nome_arquivo, fieldnames):
    caminho = OUTPUT_DIR / nome_arquivo
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados)
    print(f"✓ Gerado: {caminho} ({len(dados)} registos)")


def main():
    print("Gerando dataset de vendas angolano...")
    print("-" * 50)

    random.seed(42)  # reprodutibilidade

    clientes = gerar_clientes()
    produtos = gerar_produtos()
    vendas = gerar_vendas(clientes, produtos)

    salvar_csv(clientes, "clientes.csv", [
        "cliente_id", "nome", "cidade", "provincia", "tipo_cliente", "data_registo", "telefone"
    ])
    salvar_csv(produtos, "produtos.csv", [
        "produto_id", "nome_produto", "categoria", "preco_unitario", "unidade", "fornecedor_principal"
    ])
    salvar_csv(vendas, "vendas.csv", [
        "venda_id", "cliente_id", "produto_id", "data_venda", "quantidade",
        "preco_unitario", "valor_bruto", "desconto_percentual", "valor_desconto",
        "valor_liquido", "canal", "metodo_pagamento", "vendedor"
    ])

    print("-" * 50)
    print(f"Dataset gerado com sucesso em: {OUTPUT_DIR}")
    print(f"  - {NUM_CLIENTES} clientes")
    print(f"  - {len(produtos)} produtos")
    print(f"  - {NUM_VENDAS} vendas")
    print("Moeda: Kwanza Angolano (AOA)")


if __name__ == "__main__":
    main()
