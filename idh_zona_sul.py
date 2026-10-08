bairros_idh = {
    "Barra da Tijuca": 0.959,
    "Copacabana": 0.956,
    "Tijuca": 0.926,
    "Botafogo": 0.952,
    "Flamengo": 0.959,
    "Ipanema": 0.962,
    "Gávea": 0.970,
    "Laranjeiras": 0.957,
    "Jardim Guanabara": 0.963,
    "Leblon": 0.967,
    "Humaitá": 0.800,
    "Leme": 0.955,
    "Lagoa": 0.959,
    "Jardim Botânico": 0.957
}

# Calculando o IDH médio
soma_idh = sum(bairros_idh.values())
quantidade_bairros = len(bairros_idh)
idh_medio = soma_idh / quantidade_bairros

# Exibindo os resultados
print("IDH por bairro:")

for bairro, idh in bairros_idh.items():
    print(f"  {bairro}: {idh:.3f}")

print(f"\nIDH médio dos bairros: {idh_medio:.3f}")