import numpy as np
from CargaConcentrada import *
from Ponto import *

class Barra:
    def __init__(self, inicio, fim, E, G, Ax, Ix, Iy, Iz, alfa, rotulaInicio, rotulaFim):
        self.inicio = inicio
        self.fim = fim
        self.comprimento = ((inicio.x - fim.x)**2 + (inicio.y - fim.y)**2 + (inicio.z - fim.z)**2)**(1/2)
        self.E = E
        self.G = G
        self.Ax = Ax
        self.Ix = Ix
        self.Iy = Iy
        self.Iz = Iz
        self.alfa = np.radians(alfa)
        self.rotulaInicio = rotulaInicio
        self.rotulaFim = rotulaFim
        self.cargas = []
        self.matriz = [
            [E*Ax/self.comprimento, 0,0,0,0,0, -E*Ax/self.comprimento, 0,0,0,0,0],
            [0, 12*E*Iz/self.comprimento**3, 0,0,0, 6*E*Iz/self.comprimento**2, 0, -12*E*Iz/self.comprimento**3, 0,0,0, 6*E*Iz/self.comprimento**2],
            [0,0, 12*E*Iy/self.comprimento**3, 0, -6*E*Iy/self.comprimento**2, 0,0,0, -12*E*Iy/self.comprimento**3, 0, -6*E*Iy/self.comprimento**2, 0],
            [0,0,0, G*Ix/self.comprimento, 0,0,0,0,0, -G*Ix/self.comprimento, 0,0],
            [0,0, -6*E*Iy/self.comprimento**2, 0, 4*E*Iy/self.comprimento, 0,0,0, 6*E*Iy/self.comprimento**2, 0, 2*E*Iy/self.comprimento, 0],
            [0, 6*E*Iz/self.comprimento**2, 0,0,0, 4*E*Iz/self.comprimento, 0, -6*E*Iz/self.comprimento**2, 0,0,0, 2*E*Iz/self.comprimento],
            [-E*Ax/self.comprimento, 0,0,0,0,0, E*Ax/self.comprimento, 0,0,0,0,0],
            [0, -12*E*Iz/self.comprimento**3, 0,0,0, -6*E*Iz/self.comprimento**2, 0, 12*E*Iz/self.comprimento**3, 0,0,0, -6*E*Iz/self.comprimento**2],
            [0,0, -12*E*Iy/self.comprimento**3, 0, 6*E*Iy/self.comprimento**2, 0,0,0, 12*E*Iy/self.comprimento**3, 0, 6*E*Iy/self.comprimento**2, 0],
            [0,0,0, -G*Ix/self.comprimento, 0,0,0,0,0, G*Ix/self.comprimento, 0,0],
            [0,0, -6*E*Iy/self.comprimento**2, 0, 2*E*Iy/self.comprimento, 0,0,0, 6*E*Iy/self.comprimento**2, 0, 4*E*Iy/self.comprimento, 0],
            [0, 6*E*Iz/self.comprimento**2, 0,0,0, 2*E*Iz/self.comprimento, 0, -6*E*Iz/self.comprimento**2, 0,0,0, 4*E*Iz/self.comprimento]
        ]    
        
    def matrizR(self):
        Cx = (self.fim.x - self.inicio.x)/self.comprimento
        Cy = (self.fim.y - self.inicio.y)/self.comprimento
        Cz = (self.fim.z - self.inicio.z)/self.comprimento
        Cxz = (Cx**2 + Cz**2)**(1/2)
        cosa = np.cos(self.alfa)
        sena = np.sin(self.alfa)
        if self.inicio.x == self.fim.x and self.inicio.z == self.fim.z:
            R = [
                [0, Cy, 0],
                [-Cy*cosa, 0, sena],
                [Cy*sena, 0, cosa]
                ]
        else:
            R = [
                [Cx, Cy, Cz],
                [(-Cx*Cy*cosa - Cz*sena)/Cxz, Cxz*cosa, (-Cy*Cz*cosa + Cx*sena)/Cxz],
                [(Cx*Cy*sena - Cz*cosa)/Cxz, -Cxz*sena, (Cy*Cz*sena + Cx*cosa)/Cxz]
                ]
        return R

    def matrizRotacao(self):
        R = self.matrizR()
        matrizRot = []
        for i in range(0, 12):
            matrizRot.append([])
            for j in range(0, 12):
                matrizRot[i].append(0)
        for i in range(0, 12, 3):
            for j in range(0, 3):
                for k in range(0,3):    
                    matrizRot[i+k][i+j] = R[k][j]
        return matrizRot

    def __zerarRigidez(self, indice, matriz):
        for i in range(0,12):
            matriz[indice][i] = 0
            matriz[i][indice] = 0
        return matriz 

    def matrizRigidezGlobal(self):
        matrizLocal = self.matriz
        if(self.rotulaInicio != None):
            if self.rotulaInicio.x == 1 :
                matrizLocal = self.__zerarRigidez(3, matrizLocal)
            if self.rotulaInicio.y == 1 :
                matrizLocal = self.__zerarRigidez(4, matrizLocal)
            if self.rotulaInicio.z == 1 :
                matrizLocal = self.__zerarRigidez(5, matrizLocal)

        if(self.rotulaFim != None):
            if self.rotulaFim.x == 1 :
                matrizLocal = self.__zerarRigidez(9, matrizLocal)
            if self.rotulaFim.y == 1 :
                matrizLocal = self.__zerarRigidez(10, matrizLocal)
            if self.rotulaFim.z == 1 :
                matrizLocal = self.__zerarRigidez(11, matrizLocal)

        rotacaoTransposta = np.transpose(self.matrizRotacao())
        matrizRigidezGlobal = np.dot(np.dot(rotacaoTransposta, matrizLocal), self.matrizRotacao())
        return matrizRigidezGlobal

    def addCarga(self, carga):
        self.cargas.append(carga)

    def distParaConc(self):
        cargasConcentradas = []
        for carga in self.cargas:
            if type(carga) is CargaConcentrada:
                cargasConcentradas.append(carga)
            else:
                novaCarga = CargaConcentrada(carga.distanciaNoInicio + carga.comprimento/2, 
                                             carga.valor*carga.comprimento, carga.tipo)
                cargasConcentradas.append(novaCarga)
        return cargasConcentradas

    def cargaTransversalParaNo(self, carga):
        reacoes = [[],[],[],[],[]]
        a = carga.distanciaNoInicio
        b = self.comprimento - a
        reacoes[0] = carga.valor * b**2 * (3*a+b) / self.comprimento**3
        reacoes[1] = carga.valor * a**2 * (a+3*b) / self.comprimento**3
        reacoes[2] = -carga.valor * a * b**2 / self.comprimento**2
        reacoes[3] = 1 * carga.valor * a**2 * b / self.comprimento**2
        return reacoes

    def momentoParaNo(self, carga):
        reacoes = [[],[],[],[],[]]
        a = carga.distanciaNoInicio
        b = self.comprimento - a
        reacoes[0] = 6 * carga.valor * a*b / self.comprimento**3
        reacoes[1] = -6 * carga.valor * a*b / self.comprimento**3
        reacoes[2] = -carga.valor * b * (2*a-b) / self.comprimento**2
        reacoes[3] = -carga.valor * a * (2*b-a) / self.comprimento**2
        return reacoes
    
    def reacoesAsCargas(self):
        reacoesAsCargas = [
            [0],[0],[0],[0],[0],[0],
            [0],[0],[0],[0],[0],[0]
            ]
        cargas = self.distParaConc()
        for carga in cargas:
            if  carga.tipo == 0:
                reacoesAsCargas[0][0] += carga.valor/2
                reacoesAsCargas[6][0] += carga.valor/2
            elif carga.tipo == 1:
                reacoes = self.cargaTransversalParaNo(carga)
                reacoesAsCargas[1][0] += reacoes[0]
                reacoesAsCargas[7][0] += reacoes[1]
                reacoesAsCargas[5][0] += reacoes[2]
                reacoesAsCargas[11][0] += reacoes[3]
            elif carga.tipo == 2:
                reacoes = self.cargaTransversalParaNo(carga)
                reacoesAsCargas[2][0] += reacoes[0]
                reacoesAsCargas[8][0] += reacoes[1]
                reacoesAsCargas[4][0] += reacoes[2]
                reacoesAsCargas[10][0] += reacoes[3]
            elif carga.tipo == 3:
                a = carga.distanciaNoInicio
                b = self.comprimento - a
                reacoesAsCargas[3][0] = carga.valor * b / self.comprimento
                reacoesAsCargas[3][0] = carga.valor * a / self.comprimento
            elif carga.tipo == 4:
                reacoes = self.momentoParaNo(carga)
                reacoesAsCargas[2][0] += reacoes[0]
                reacoesAsCargas[8][0] += reacoes[1]
                reacoesAsCargas[4][0] += reacoes[2]
                reacoesAsCargas[10][0] += reacoes[3]
            elif carga.tipo == 5:
                reacoes = self.momentoParaNo(carga)
                reacoesAsCargas[1][0] += reacoes[0]
                reacoesAsCargas[7][0] += reacoes[1]
                reacoesAsCargas[5][0] += reacoes[2]
                reacoesAsCargas[11][0] += reacoes[3]

        return reacoesAsCargas