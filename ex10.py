real = float(input('Quanto dinheiro você tem na carteira? R$ '))
dolar = real / 5.15
print('Com R${:.2f} voê pode cpmprar US${:.2f}'.format(real, dolar))