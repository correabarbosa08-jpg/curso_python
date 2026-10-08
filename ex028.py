from random import randint

computador = randint(0, 5)
print('Vou pensar em um número entre 0 e 5. Tente adivinhar...')
jogador = int(input('Em que número eu pensei? '))
if jogador == computador:
    print('PARABÉNS! Você venceu! Eu pensei no número {}.'.format(computador))
else:
    print('Você perdeu! Eu pensei no número {} e não no {}.'.format(computador, jogador))
