nome = str(input('Digite seu nome completo: ')).strip()

print(f'Nome em maiúsculas: {nome.upper()}')
print(f'Quantidade de letras (sem espaços): {len(nome.replace(" ", ""))}')

primeiro_nome = nome.split()[0]
print(f'O primeiro nome tem {len(primeiro_nome)} letras')
