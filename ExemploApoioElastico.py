from Barra import *
from CargaConcentrada import *
from CargaDistribuida import *
from Ponto import *
from Estrutura import *
from Plot import *
from DeslocamentoPrescrito import *
from ApoioElastico import *

p0 = Ponto(0,0,0,1,1,1,1,1,1)
p1 = Ponto(3000,0,0,0,0,0,0,0,0)

p1.adicionarApoioElastico(ApoioElastico(1,10/1000))

e = 100000 * 1000
g = 82
ax = 10000
ix = 8.3333 
iy = ix
iz = iy

b0 = Barra(p0,p1,e,g,ax,ix,iy,iz,0,None,None)
b0.addCarga(CargaConcentrada(1500,-10,1))
pontos = [p0,p1]
barras = [b0]


estrutura = Estrutura(barras, pontos)

#print(estrutura.cargasNodaisCombinadas())
print("Reações de apoio: ", estrutura.reacoesDeApoio())
#print("Reações 2: ", estrutura.segundaOpcaoReacoes())
#print("Reações 2: ", estrutura.segundaOpcaoReacoes())
#print("Deslocamentos: ", estrutura.deslocamentos())
#print("Esforços: ", estrutura.esforcos())