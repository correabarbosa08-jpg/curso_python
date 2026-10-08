cidade = input('Digite o nome de uma cidade: ').strip()
primeira_palavra = cidade.upper().split()[0] if cidade else ''
print(f'A cidade começa com "SANTO"? {primeira_palavra == "SANTO"}')