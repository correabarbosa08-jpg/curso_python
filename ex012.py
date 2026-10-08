preço = float(input('qual é o preço do produto? R$'))
novo = preço - (preço * 5 / 100)
print ('o produto que custava R${}, na promoção vai custar R${}'.format(preço, novo))