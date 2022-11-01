from Barra import *
from CargaConcentrada import *
from CargaDistribuida import *
from Ponto import *
from Estrutura import *
from Plot import *
from Rotula import *



p = -10
l = 4

e = 206.84*1000000
g = 82.74*1000000
ax = 70.97 / 10000
ix = 3452.8 / 100000000
iy = 2329.6 / 100000000
iz = iy

p0 = Ponto(0,0,0,1,1,1,1,1,1)
p1 = Ponto(l,0,0,0,0,0,0,0,0)
p2 = Ponto(2*l,0,0,0,1,0,0,0,0)

r0 = Rotula(0,0,1)

b0 = Barra(p0,p1,e,g,ax,ix,iy,iz,0,None,r0)
b1 = Barra(p1,p2,e,g,ax,ix,iy,iz,0,None,None)

b0.addCarga(CargaConcentrada(l/2,p, 1))
b1.addCarga(CargaDistribuida(0,l,p,1))

pontos = [p0,p1,p2]
barras = [b0,b1]


estrutura = Estrutura(barras, pontos)




#for barra in estrutura.barras:
#    print(barra.matrizR())

#matrizRigidez = estrutura.matrizRigidez()
#for linha in matrizRigidez:
#    print(linha)
#print()
#for barra in estrutura.barras:
#    print(barra.reacoesAsCargas())
#print(estrutura.cargasNodaisEquivalentes())
#print(estrutura.cargasNodais())
#print("---------------------")
#print(estrutura.cargasNodaisCombinadas())


#deslocamentos = estrutura.deslocamentos()
#print(deslocamentos)

    
reacoes = estrutura.reacoesDeApoio()
print(reacoes)
print("-----------")
#esforcos = estrutura.esforcos()
#for linha in esforcos:
#    print(linha)
#    print()




