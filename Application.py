from barra import *
from cargaConcentrada import CargaConcentrada
from cargaDist import *
from ponto import *
from estrutura import *



p0 = Ponto(100,0,0,0,0,0,-10,-1000)
p1 = Ponto(0,0,1,1,1,0,0,0)
p2 = Ponto(200,-3*100/4,1,1,1,0,0,0)


b0 = Barra(p1,p0,10000*1000, 10000*10)
b0.addCarga(CargaDistribuida(0,100,-2.4*10/100))
b1 = Barra(p0,p2,10000*1000,10000*10)
b1.addCarga(CargaConcentrada(5*100/8,6*10/5,0))
b1.addCarga(CargaConcentrada(5*100/8,-8*10/5,1))


pontos = [p0,p1,p2]
barras = [b0,b1]


estrutura = Estrutura(barras, pontos)

matrizRigidez = estrutura.matrizRigidez()
for linha in matrizRigidez:
    print(linha)
print()
for barra in estrutura.barras:
    print(barra.reacoesAsCargas())
print(estrutura.cargasNodaisEquivalentes())
print(estrutura.cargasNodais())
print(estrutura.cargasNodaisCombinadas())


deslocamentos = estrutura.deslocamentos()
print(deslocamentos)


reacoesDeApoio = estrutura.reacoesDeApoio()
print(reacoesDeApoio)
print()

esforcos = estrutura.esforcos()
for linha in esforcos:
    print(linha)
print()





