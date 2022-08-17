from barra import *
from cargaConcentrada import CargaConcentrada
from cargaDist import *
from ponto import *
from estrutura import *



p = 60


p0 = Ponto(0,3,0,0,0,0,0,0,0)
p1 = Ponto(6,3,0,0,0,0,0,0,0)
p2 = Ponto(0,0,0,1,1,1,1,1,1)
p3 = Ponto(9,0,3,1,1,1,1,1,1)

p0.adicionarCarga(2*p, 0)
p1.adicionarCarga(-p,1)
p1.adicionarCarga(-3*p,5)

b0 = Barra(p0,p1,200000000,80000000,0.01,2/1000,1/1000,1/1000,0)
b1 = Barra(p2,p0,200000000,80000000,0.01,2/1000,1/1000,1/1000,0)
b2 = Barra(p1,p3,200000000,80000000,0.01,2/1000,1/1000,1/1000,0)
b0.addCarga(CargaConcentrada(3,4*p,2))

pontos = [p0,p1,p2,p3]
barras = [b0,b1,b2]


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


reacoesDeApoio = estrutura.reacoesDeApoio()
print(reacoesDeApoio)

#esforcos = estrutura.esforcos()
#for linha in esforcos:
#    print(linha)
#    print()
#print()



