import numpy as np

class Estrutura:
    def __init__(self, barras, pontos):
        self.barras = barras
        self.pontos = pontos
    
    def matrizRigidez(self):
        v = 6 #vinculos por nó
        matrizEstrutura = []
        #Faz a matriz zerada
        for i in range(0, len(self.pontos)*v):
            matrizEstrutura.append([])
            for j in range(len(self.pontos)*v):
                matrizEstrutura[i].append(0)
        
        #Preenche a matriz
        for barra in self.barras:
            matrizBarra = barra.matrizRigidezGlobal()
            inicio = self.pontos.index(barra.inicio) * v
            fim = self.pontos.index(barra.fim) * v

            for j in range(v):
                for k in range(v):
                    matrizEstrutura[inicio+j][inicio+k] += matrizBarra[j][k]
                    matrizEstrutura[fim+j][fim+k] += matrizBarra[j+v][k+v]
                    matrizEstrutura[inicio+j][fim+k] += matrizBarra[j][k+v]
                    matrizEstrutura[fim+j][inicio+k] += matrizBarra[j+v][k] 
            
            pontos = self.pontos
            for i in range(0, len(pontos)):
                for apoioElastico in pontos[i].apoiosElasticos:
                    indice = i*v+apoioElastico.vinculo
                    matrizEstrutura[indice][indice] += apoioElastico.valor

        return matrizEstrutura

    def cargasNodais(self):
        cargasNodais = []
        for ponto in self.pontos:
            for i in range(0,6):
                cargasNodais.append([ponto.cargas[i]])
        return cargasNodais

    def cargasNodaisEquivalentes(self):
        v = 6 #vinculos por nó
        cargasNodaisEquivalentes = []
        for ponto in self.pontos:
            for i in range(v):
                cargasNodaisEquivalentes.append([0])

        for barra in self.barras:
            cargasEquivalentes = np.dot(np.transpose(barra.matrizRotacao()), barra.reacoesAsCargas())
            inicio = self.pontos.index(barra.inicio)
            fim = self.pontos.index(barra.fim)
            
            cargasNodaisEquivalentes[v*inicio][0] -= cargasEquivalentes[0][0]
            cargasNodaisEquivalentes[v*inicio+1][0] -= cargasEquivalentes[1][0]
            cargasNodaisEquivalentes[v*inicio+2][0] -= cargasEquivalentes[2][0]
            cargasNodaisEquivalentes[v*inicio+3][0] -= cargasEquivalentes[3][0]
            cargasNodaisEquivalentes[v*inicio+4][0] -= cargasEquivalentes[4][0]
            cargasNodaisEquivalentes[v*inicio+5][0] -= cargasEquivalentes[5][0]
            
            cargasNodaisEquivalentes[v*fim][0] -= cargasEquivalentes[6][0]
            cargasNodaisEquivalentes[v*fim+1][0] -= cargasEquivalentes[7][0]
            cargasNodaisEquivalentes[v*fim+2][0] -= cargasEquivalentes[8][0]
            cargasNodaisEquivalentes[v*fim+3][0] -= cargasEquivalentes[9][0]
            cargasNodaisEquivalentes[v*fim+4][0] -= cargasEquivalentes[10][0]
            cargasNodaisEquivalentes[v*fim+5][0] -= cargasEquivalentes[11][0]

        return cargasNodaisEquivalentes

    def cargasNodaisCombinadas(self):
        v = 6 #vinculos por nó
        cargasNodais = self.cargasNodais()
        cargasNodaisEquivalentes = self.cargasNodaisEquivalentes()
        cargasNodaisCombinadas = []
        for i in range(0, len(self.pontos) * v):
            cargasNodaisCombinadas.append([cargasNodais[i][0] + cargasNodaisEquivalentes[i][0]])

        return cargasNodaisCombinadas

    def __indicesNulos(self):
        v = 6
        indicesNulos = []
        for i in range(0, len(self.pontos)):
            if self.pontos[i].restricaoLinearX == 0:
                indicesNulos.append(v*i)
            if self.pontos[i].restricaoLinearY == 0:
                indicesNulos.append(v*i+1)
            if self.pontos[i].restricaoLinearZ == 0:
                indicesNulos.append(v*i+2)
            if self.pontos[i].restricaoRotacaoX == 0:
                indicesNulos.append(v*i+3)
            if self.pontos[i].restricaoRotacaoY == 0:
                indicesNulos.append(v*i+4)
            if self.pontos[i].restricaoRotacaoZ == 0:
                indicesNulos.append(v*i+5)
        return indicesNulos

    def __indicesRestritos(self):
        v = 6
        vinculosRestringidos = []
        for i in range(len(self.pontos)):
            if self.pontos[i].restricaoLinearX == 1:
                vinculosRestringidos.append(v*i)
            if self.pontos[i].restricaoLinearY == 1:
                vinculosRestringidos.append(v*i+1)
            if self.pontos[i].restricaoLinearZ == 1:
                vinculosRestringidos.append(v*i+2)
            if self.pontos[i].restricaoRotacaoX == 1:
                vinculosRestringidos.append(v*i+3)
            if self.pontos[i].restricaoRotacaoY == 1:
                vinculosRestringidos.append(v*i+4)
            if self.pontos[i].restricaoRotacaoZ == 1:
                vinculosRestringidos.append(v*i+5)
        return vinculosRestringidos

    def deslocamentos(self):
        v = 6 #vinculos por nó
        matrizGlobal = self.matrizRigidez()
        matrizSistema = []
        indicesNulos = self.__indicesNulos()
        matrizCargas = []
        
        for i in range(0, len(indicesNulos)):
            matrizSistema.append([])
            for j in range(len(indicesNulos)):
                matrizSistema[i].append(matrizGlobal[indicesNulos[i]][indicesNulos[j]])
        
        cargasNodaisCombinadas = self.cargasNodaisCombinadas() 
    
        for indice in indicesNulos:
            cargaDesloc = 0
            for i in range(0, len(self.pontos)):
                for desloc in self.pontos[i].deslocamentosPrescritos:
                    cargaDesloc += matrizGlobal[indice][i*v+desloc.vinculo] * desloc.valor
            matrizCargas.append([cargasNodaisCombinadas[indice][0] - cargaDesloc])
        
        matrizSistema = np.array(matrizSistema)
        matrizCargas = np.array(matrizCargas)

        if ( len(matrizCargas) > 0 and len(matrizSistema) > 0):
            resultadoDeslocamentos = np.linalg.solve(matrizSistema, matrizCargas)
        else: resultadoDeslocamentos = []
        deslocamentos = []
        for ponto in self.pontos:
            for i in range(v):
                deslocamentos.append(0)
            
        for i in range(0, len(indicesNulos)):
            deslocamentos[indicesNulos[i]] = resultadoDeslocamentos[i][0]
        for i in range(0, len(self.pontos)):
            for desloc in self.pontos[i].deslocamentosPrescritos:
                deslocamentos[i*v+desloc.vinculo] = desloc.valor
        return deslocamentos

    def segundaOpcaoReacoes(self):
        matrizRigidez = self.matrizRigidez()
        cargasNodaisCombinadas = self.cargasNodaisCombinadas()
        deslocamentosInicial = self.deslocamentos()
        deslocamentos = []
        for deslocamento in deslocamentosInicial:
            deslocamentos.append([deslocamento])
        matrizRigidez = np.array(matrizRigidez)
        cargasNodaisCombinadas = np.array(cargasNodaisCombinadas)
        deslocamentos = np.array(deslocamentos)
        resultado = np.matmul(matrizRigidez, deslocamentos)
        resultado = np.subtract(resultado, cargasNodaisCombinadas)
        return resultado

    def reacoesDeApoio(self):
        v = 6 #vinculos por nó
        matrizRigidez = self.matrizRigidez()
        cargasNodaisCombinadas = self.cargasNodaisCombinadas()
        deslocamentos = self.deslocamentos()
        reacoesDeApoio = []
        for ponto in self.pontos:
            for i in range(v):
                reacoesDeApoio.append(0)

        vinculosLivres = self.__indicesNulos()
        vinculosRestringidos = self.__indicesRestritos()
        
        for vinculoRestrito in vinculosRestringidos:
            reacoesDeApoio[vinculoRestrito] -=  cargasNodaisCombinadas[vinculoRestrito][0]
            for restrito in vinculosRestringidos:
                reacoesDeApoio[vinculoRestrito] += matrizRigidez[vinculoRestrito][restrito] * deslocamentos[restrito]
            for vinculoLivre in vinculosLivres:
                reacoesDeApoio[vinculoRestrito] += matrizRigidez[vinculoRestrito][vinculoLivre] * deslocamentos[vinculoLivre]
        
        pontos = self.pontos
        for i in range(0, len(pontos)):
            for apoioElastico in pontos[i].apoiosElasticos:
                indice = i*v+apoioElastico.vinculo
                reacoesDeApoio[indice] -= deslocamentos[indice]*apoioElastico.valor
        
        return reacoesDeApoio

    def esforcos(self):
        v = 6 #vinculos por nó
        deslocamentosGeral = self.deslocamentos()
        esforcos = []
        deslocamentos = []
        for barra in self.barras:
            inicio = self.pontos.index(barra.inicio)
            fim = self.pontos.index(barra.fim)
            
            deslocamentos = [[deslocamentosGeral[v*inicio]], 
                             [deslocamentosGeral[v*inicio + 1]],
                             [deslocamentosGeral[v*inicio + 2]],
                             [deslocamentosGeral[v*inicio + 3]],
                             [deslocamentosGeral[v*inicio + 4]],
                             [deslocamentosGeral[v*inicio + 5]],
                             [deslocamentosGeral[v*fim]],
                             [deslocamentosGeral[v*fim + 1]],
                             [deslocamentosGeral[v*fim + 2]],
                             [deslocamentosGeral[v*fim + 3]],
                             [deslocamentosGeral[v*fim + 4]],
                             [deslocamentosGeral[v*fim + 5]]]
            
            deslocamentos = np.dot(barra.matrizRotacao(), deslocamentos)

            matrizRigidezBarra = barra.matriz
            reacoes = barra.reacoesAsCargas() 

            esforcoBarra = []
            for i in range(0, 2*v):
                esforcoBarra.append(reacoes[i][0])
                for j in range(0, 2*v):
                    esforcoBarra[i] += matrizRigidezBarra[i][j] * deslocamentos[j][0]
                if i > 5: esforcoBarra[i] = -esforcoBarra[i]
            esforcos.append(esforcoBarra)
        return esforcos

    def equacoes(self,tipo):
        equacoes = []
        esforcos = self.esforcos()
        barras = self.barras
        for i in range(0,len(barras)):
            inicio = esforcos[i][tipo]
            fim = esforcos[i][tipo+6]
            diferenca = inicio-fim
            if diferenca == 0:
                equacoes.append("f(x) = " + str(inicio))
            else:
                equacoes.append("f(x) = " + str(diferenca/barras[i].comprimento) + "X + " + str(inicio))
        return equacoes


            



