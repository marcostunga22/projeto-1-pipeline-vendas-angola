import pandas as pd
df = pd.DataFrame([
    ["Luanda", 120000], ["Benguela", 85000],
    ["Huila", 62000], ["Huambo", 45000],
])
df.columns = ["provincia", "vendas_kz"]
print(df)
print("Total:", df["vendas_kz"].sum())    
df.to_csv("resultado.csv", index=False)
