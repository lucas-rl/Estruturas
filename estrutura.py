import numpy as np


class Estrutura:
    def __init__(self, barras, pontos):
        self.barras = barras
        self.pontos = pontos
    
    def matrizRigidez(self):
        v = 3 #vinculos por nó
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
        return matrizEstrutura

    def cargasNodais(self):
        cargasNodais = []
        for ponto in self.pontos:
            cargasNodais.append([ponto.cargaHorizontal])
            cargasNodais.append([ponto.cargaVertical])
            cargasNodais.append([ponto.cargaRotacao])
        return cargasNodais

    def cargasNodaisEquivalentes(self):
        v = 3 #vinculos por nó
        cargasNodaisEquivalentes = []
        for ponto in self.pontos:
            for i in range(v):
                cargasNodaisEquivalentes.append([0])

        for barra in self.barras:
            cargasEquivalentes = np.dot(np.transpose(barra.matrizRotacao), barra.reacoesAsCargas())
            inicio = self.pontos.index(barra.inicio)
            fim = self.pontos.index(barra.fim)
            
            cargasNodaisEquivalentes[v*inicio][0] += cargasEquivalentes[0][0]
            cargasNodaisEquivalentes[v*inicio+1][0] += cargasEquivalentes[1][0]
            cargasNodaisEquivalentes[v*inicio+2][0] += cargasEquivalentes[2][0]
            cargasNodaisEquivalentes[v*fim][0] += cargasEquivalentes[3][0]
            cargasNodaisEquivalentes[v*fim+1][0] += cargasEquivalentes[4][0]
            cargasNodaisEquivalentes[v*fim+2][0] += cargasEquivalentes[5][0]
        
        return cargasNodaisEquivalentes

    def cargasNodaisCombinadas(self):
        v = 3 #vinculos por nó
        cargasNodais = self.cargasNodais()
        cargasNodaisEquivalentes = self.cargasNodaisEquivalentes()
        cargasNodaisCombinadas = []
        for i in range(0, len(self.pontos) * v):
            cargasNodaisCombinadas.append([cargasNodais[i][0] + cargasNodaisEquivalentes[i][0]])

        return cargasNodaisCombinadas

    def deslocamentos(self):
        v = 3 #vinculos por nó
        matrizGlobal = self.matrizRigidez()
        matrizSistema = []
        indicesNulos = []
        matrizCargas = []
        
        for i in range(0, len(self.pontos)):
            if self.pontos[i].horizontal == 0:
                indicesNulos.append(v*i)
            if self.pontos[i].vertical == 0:
                indicesNulos.append(v*i+1)
            if self.pontos[i].rotacao == 0:
                indicesNulos.append(v*i+2)
        
        for i in range(0, len(indicesNulos)):
            matrizSistema.append([])
            for j in range(len(indicesNulos)):
                matrizSistema[i].append(matrizGlobal[indicesNulos[i]][indicesNulos[j]])
        
        for indice in indicesNulos:
            matrizCargas.append(self.cargasNodaisCombinadas()[indice])
        
        matrizSistema = np.array(matrizSistema)
        matrizCargas = np.array(matrizCargas)
        
        resultadoDeslocamentos = np.linalg.solve(matrizSistema, matrizCargas)

        deslocamentos = []
        for ponto in self.pontos:
            for i in range(v):
                deslocamentos.append(0)
            
        
        for i in range(len(indicesNulos)):
            deslocamentos[indicesNulos[i]] = resultadoDeslocamentos[i][0]

        return deslocamentos

    def reacoesDeApoio(self):
        v = 3 #vinculos por nó
        matrizRigidez = self.matrizRigidez()
        cargasNodaisCombinadas = self.cargasNodaisCombinadas()
        deslocamentos = self.deslocamentos()
        reacoesDeApoio = []
        for ponto in self.pontos:
            for i in range(v):
                reacoesDeApoio.append(0)

        vinculosLivres = []
        for i in range(len(self.pontos)):
            if self.pontos[i].horizontal == 0:
                vinculosLivres.append(v*i)
            if self.pontos[i].vertical == 0:
                vinculosLivres.append(v*i+1)
            if self.pontos[i].rotacao == 0:
                vinculosLivres.append(v*i+2)

        vinculosRestringidos = []
        for i in range(len(self.pontos)):
            if self.pontos[i].vertical == 1:
                vinculosRestringidos.append(v*i)
            if self.pontos[i].vertical == 1:
                vinculosRestringidos.append(v*i+1)
            if self.pontos[i].rotacao == 1:
                vinculosRestringidos.append(v*i+2)
        
        for vinculoRestrito in vinculosRestringidos:
            reacoesDeApoio[vinculoRestrito] -=  cargasNodaisCombinadas[vinculoRestrito][0]
            print()
            for vinculoLivre in vinculosLivres:
                reacoesDeApoio[vinculoRestrito] += matrizRigidez[vinculoRestrito][vinculoLivre] * deslocamentos[vinculoLivre]
        
        return reacoesDeApoio

    def esforcos(self):
        v = 3 #vinculos por nó
        deslocamentosGeral = self.deslocamentos()
        esforcos = []
        deslocamentos = []
        for barra in self.barras:
            inicio = self.pontos.index(barra.inicio)
            fim = self.pontos.index(barra.fim)
            
            deslocamentos = [[deslocamentosGeral[v*inicio]], 
                             [deslocamentosGeral[v*inicio + 1]],
                             [deslocamentosGeral[v*inicio + 2]],
                             [deslocamentosGeral[v*fim]],
                             [deslocamentosGeral[v*fim + 1]],
                             [deslocamentosGeral[v*fim + 2]]]
            
            deslocamentos = np.dot(barra.matrizRotacao, deslocamentos)

            matrizRigidezBarra = barra.matriz
            reacoes = barra.reacoesAsCargas() 
            print(reacoes)

            esforcoBarra = []
            for i in range(0, 2*v):
                esforcoBarra.append([-reacoes[i][0]])
                for j in range(0, 2*v):
                    esforcoBarra[i][0] += matrizRigidezBarra[i][j] * deslocamentos[j][0]
            esforcos.append(esforcoBarra)
        return esforcos






