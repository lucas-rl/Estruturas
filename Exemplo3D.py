from Barra import *
from CargaConcentrada import *
from CargaDistribuida import *
from Ponto import *
from Estrutura import *
from Plot import *



p = 4.448
l = 3.048

e = 206.84*1000000
g = 82.74*1000000
ax = 70.97 / 10000
ix = 3452.8 / 100000000
iy = 2329.6 / 100000000
iz = iy

p0 = Ponto(0,0,0,1,1,1,1,1,1)
p1 = Ponto(0,l,0,0,0,0,0,0,0)
p2 = Ponto(2*l,l,0,0,0,0,0,0,0)
p3 = Ponto(3*l,0,l,1,1,1,1,1,1)

p1.adicionarCarga(2*p, 0)
p2.adicionarCarga(-p,1)
p2.adicionarCarga(-l*p,5)

b0 = Barra(p0,p1,e,g,ax,ix,iy,iz,0,None,None)
b1 = Barra(p1,p2,e,g,ax,ix,iy,iz,0,None,None)
b2 = Barra(p2,p3,e,g,ax,ix,iy,iz,0,None,None)
b1.addCarga(CargaConcentrada(l, 4*p, 2))

pontos = [p0,p1,p2,p3]
barras = [b0,b1,b2]


estrutura = Estrutura(barras, pontos)

#print(b1.reacoesAsCargas())
#print(estrutura.cargasNodaisEquivalentes())
#print("---------")
#print(estrutura.cargasNodaisCombinadas())

#print(estrutura.cargasNodais())
#print("------")
print("Reaçoes de apoio: ", estrutura.reacoesDeApoio())
#print("Reações 2: ", estrutura.segundaOpcaoReacoes())
#print("--------")
#print("Deslocamentos: ", estrutura.deslocamentos())



