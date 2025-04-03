shoplist = [['apple'],['mango'],['carrot', 'radish'], ['banana']]
copylist = shoplist

print(f'{copylist is shoplist}, {id(shoplist)=}, {id(copylist)=}')

print(f'{shoplist=}')
print(f'{copylist=}')

del shoplist[0]
print(f'{shoplist=}')
print(f'{copylist=}')

del copylist[-1]
print(f'{shoplist=}')
print(f'{copylist=}')

del copylist[-1][0]
print(f'{shoplist=}')
print(f'{copylist=}')