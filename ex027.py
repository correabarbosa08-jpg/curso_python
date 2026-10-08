nome = str(input('Digite seu nome completo: ')).strip()
nome_separado = nome.split()

primeiro_nome = nome_separado[0]
ultimo_nome = nome_separado[-1]

print('Muito prazer, seu primeiro nome é {} e seu último nome é {}'.format(primeiro_nome, ultimo_nome))
