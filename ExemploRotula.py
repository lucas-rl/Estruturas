from Barra import *
from CargaConcentrada import *
from CargaDistribuida import *
from Ponto import *
from Estrutura import *
from Plot import *
from Rotula import *



p = -10
l = 1.5

e = 100000 * 1000
g = 82
ax = 10000
ix = 8.3333 
iy = ix
iz = iy

p0 = Ponto(0,0,0,1,1,1,1,1,1)
p1 = Ponto(l,0,0,0,0,0,0,0,0)
p2 = Ponto(2*l,0,0,0,1,0,0,0,0)

r0 = Rotula(0,0,1)

b0 = Barra(p0,p1,e,g,ax,ix,iy,iz,0,None,None)
b1 = Barra(p1,p2,e,g,ax,ix,iy,iz,0,r0,None)

b0.addCarga(CargaConcentrada(l/2,p, 1))
b1.addCarga(CargaConcentrada(l/2,p, 1))


pontos = [p0,p1,p2]
barras = [b0,b1]


estrutura = Estrutura(barras, pontos)

    
print(estrutura.reacoesDeApoio())
#print(estrutura.deslocamentos())




