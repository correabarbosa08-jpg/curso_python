salário = float(input('Qual é o salário do funcionário? R$'))
novo = salário + (salário * 15 / 100)
print ('O funcionário que recebia R${:.2f}, com 15% de aumento, passa a receber R${:.2f}'.format(salário, novo))